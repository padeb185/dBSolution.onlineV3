"""
Stock pièces & fluides : catalogue (un OEM par pièce, plusieurs EAN), fiche avec variations de stock,
journal des mouvements, inventaires physiques et pièces utilisées par maintenance
(débitées du stock à l'émission de la facture).
"""
from core.securite import url_sure

import csv
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import DecimalField, ExpressionWrapper, F, Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache

from . import stock
from .forms_stock import InventaireForm, MouvementForm, PieceStockForm, PieceUtiliseeForm
from .models import (CategoriePiece, Fabricant, InventaireStock, LigneInventaire, MouvementStock, Piece,
                     PieceUtilisee)

# Gestion du stock (catalogue, mouvements, inventaires)
ROLES_STOCK = ["direction", "chef_mecanicien", "magasinier", "comptable"]
# Encodage des pièces utilisées dans une maintenance
ROLES_ATELIER = ROLES_STOCK + ["mecanicien", "apprentis", "carrossier", "instructeur"]


def _peut(user, roles):
    return user.is_superuser or getattr(user, "role", None) in roles


def _refuser(request):
    messages.error(request, _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


def _pieces(request):
    return Piece.objects.filter(societe=request.user.societe)


VALEUR = ExpressionWrapper(F("quantite_stock") * F("prix_achat"), output_field=DecimalField(max_digits=14, decimal_places=2))
ALERTE = Q(quantite_min__gt=0, quantite_stock__lte=F("quantite_min"))


# ---------------------------------------------------------------- catalogue
@never_cache
@login_required
def catalogue_view(request):
    if not _peut(request.user, ROLES_ATELIER):
        return _refuser(request)
    q = (request.GET.get("q") or "").strip()
    categorie = request.GET.get("categorie") or ""
    alerte = request.GET.get("alerte") == "1"
    inactives = request.GET.get("inactives") == "1"

    qs = _pieces(request).select_related("fabricant").prefetch_related("codes_barres")
    if not inactives:
        qs = qs.filter(actif=True)
    if q:
        code = stock.normaliser_code(q)
        qs = qs.filter(
            Q(oem__icontains=code) | Q(codes_barres__code__icontains=code) | Q(reference_fabricant__icontains=code)
            | Q(designation__icontains=q) | Q(organe__icontains=q) | Q(fabricant__nom__icontains=q)
            | Q(emplacement_etagere__icontains=q)
        ).distinct()
    if categorie:
        qs = qs.filter(categorie=categorie)
    if alerte:
        qs = qs.filter(ALERTE)

    actives = _pieces(request).filter(actif=True)
    totaux = {
        "nb": actives.count(),
        "valeur": actives.filter(quantite_stock__gt=0).aggregate(v=Sum(VALEUR))["v"] or Decimal("0"),
        "alertes": actives.filter(ALERTE).count(),
        "negatifs": actives.filter(quantite_stock__lt=0).count(),
    }
    page = Paginator(qs, 50).get_page(request.GET.get("page"))
    return render(request, "piece/stock/catalogue.html", {
        "page": page, "pieces": page.object_list, "q": q, "categorie": categorie, "alerte": alerte,
        "inactives": inactives, "categories": CategoriePiece.choices, "totaux": totaux,
        "peut_gerer": _peut(request.user, ROLES_STOCK),
    })


# ---------------------------------------------------------------- fiche pièce (création / modification)
def _enregistrer_piece(request, form, creation):
    with transaction.atomic():
        piece = form.save(commit=False)
        if creation:
            piece.societe = request.user.societe
        piece.fabricant = stock.fabricant_par_nom(form.cleaned_data.get("fabricant_nom"))
        if not piece.prix_vente and piece.prix_achat:
            piece.prix_vente = Decimal(str(round(piece.calcul_prix_vente(), 2)))
        piece.save()
        if piece.fabricant:
            piece.fabricants.add(piece.fabricant)
        stock.definir_eans(piece, form.cleaned_data.get("eans") or [])
        initial = form.cleaned_data.get("stock_initial") if creation else None
        if initial:
            stock.mouvement(piece, initial, MouvementStock.Type.ENTREE, utilisateur=request.user,
                            prix_unitaire=piece.prix_achat or None, commentaire=_("Stock initial"))
    return piece


@never_cache
@login_required
def piece_form_view(request, pk=None):
    if not _peut(request.user, ROLES_STOCK):
        return _refuser(request)
    piece = get_object_or_404(_pieces(request), pk=pk) if pk else None
    initial = {}
    if not piece:
        for champ in ("oem", "designation", "categorie"):
            if request.GET.get(champ):
                initial[champ] = request.GET[champ]
        if request.GET.get("ean"):
            initial["eans"] = request.GET["ean"]
    form = PieceStockForm(request.POST or None, instance=piece, societe=request.user.societe, initial=initial)
    if request.method == "POST" and form.is_valid():
        piece = _enregistrer_piece(request, form, creation=piece is None)
        messages.success(request, _("Pièce enregistrée."))
        return redirect("piece:detail", pk=piece.pk)
    return render(request, "piece/stock/piece_form.html", {
        "form": form, "piece": piece, "fabricants": Fabricant.objects.order_by("nom").values_list("nom", flat=True),
    })


@never_cache
@login_required
def piece_fiche_view(request, pk):
    if not _peut(request.user, ROLES_ATELIER):
        return _refuser(request)
    piece = get_object_or_404(_pieces(request).select_related("fabricant", "voiture_marque", "modele"), pk=pk)
    peut_gerer = _peut(request.user, ROLES_STOCK)
    form = MouvementForm(request.POST or None)
    if request.method == "POST":
        if not peut_gerer:
            return _refuser(request)
        if form.is_valid():
            t = form.cleaned_data["type_mouvement"]
            qte = form.cleaned_data["quantite"]
            if t != MouvementStock.Type.CORRECTION:
                qte = abs(qte)
                if t == MouvementStock.Type.SORTIE:
                    qte = -qte
            if qte == 0:
                messages.error(request, _("La quantité ne peut pas être nulle."))
            else:
                stock.mouvement(piece, qte, t, utilisateur=request.user,
                                prix_unitaire=form.cleaned_data.get("prix_unitaire"),
                                commentaire=form.cleaned_data.get("commentaire") or "")
                messages.success(request, _("Mouvement de stock enregistré."))
                return redirect("piece:detail", pk=piece.pk)
    mouvements = piece.mouvements.select_related("utilisateur", "maintenance", "facture")[:100]
    utilisations = piece.utilisations.select_related("maintenance", "facture").order_by("-created_at")[:50]
    return render(request, "piece/stock/piece_fiche.html", {
        "piece": piece, "form": form, "mouvements": mouvements, "utilisations": utilisations,
        "peut_gerer": peut_gerer,
    })


# ---------------------------------------------------------------- variations de stock
def _filtrer_mouvements(request):
    qs = MouvementStock.objects.filter(piece__societe=request.user.societe).select_related(
        "piece", "utilisateur", "maintenance", "facture")
    du = parse_date(request.GET.get("du") or "")
    au = parse_date(request.GET.get("au") or "")
    t = request.GET.get("type") or ""
    categorie = request.GET.get("categorie") or ""
    q = (request.GET.get("q") or "").strip()
    if du:
        qs = qs.filter(date__date__gte=du)
    if au:
        qs = qs.filter(date__date__lte=au)
    if t:
        qs = qs.filter(type_mouvement=t)
    if categorie:
        qs = qs.filter(piece__categorie=categorie)
    if q:
        code = stock.normaliser_code(q)
        qs = qs.filter(Q(piece__oem__icontains=code) | Q(piece__designation__icontains=q)
                       | Q(piece__codes_barres__code__icontains=code)).distinct()
    return qs, {"du": du, "au": au, "type": t, "categorie": categorie, "q": q}


@never_cache
@login_required
def mouvements_view(request):
    if not _peut(request.user, ROLES_STOCK):
        return _refuser(request)
    qs, filtres = _filtrer_mouvements(request)

    if request.GET.get("export") == "csv":
        reponse = HttpResponse(content_type="text/csv; charset=utf-8")
        reponse["Content-Disposition"] = 'attachment; filename="mouvements_stock.csv"'
        reponse.write("﻿")
        w = csv.writer(reponse, delimiter=";")
        w.writerow([_("Date"), _("Type"), _("Catégorie"), _("Code OEM"), _("Désignation"), _("Quantité"),
                    _("Stock avant"), _("Stock après"), _("Prix unitaire HTVA"), _("Maintenance"), _("Facture"),
                    _("Utilisateur"), _("Commentaire")])
        for m in qs:
            w.writerow([
                timezone.localtime(m.date).strftime("%d/%m/%Y %H:%M"), m.get_type_mouvement_display(),
                m.piece.get_categorie_display(), m.piece.oem, m.piece.designation,
                str(m.quantite).replace(".", ","), str(m.stock_avant).replace(".", ","),
                str(m.stock_apres).replace(".", ","),
                str(m.prix_unitaire).replace(".", ",") if m.prix_unitaire is not None else "",
                m.maintenance.immatriculation if m.maintenance_id else "",
                m.facture.numero if m.facture_id else "",
                str(m.utilisateur) if m.utilisateur_id else "", m.commentaire,
            ])
        return reponse

    entrees = qs.filter(quantite__gt=0).aggregate(s=Sum("quantite"))["s"] or Decimal("0")
    sorties = qs.filter(quantite__lt=0).aggregate(s=Sum("quantite"))["s"] or Decimal("0")
    page = Paginator(qs, 50).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    return render(request, "piece/stock/mouvements.html", {
        "page": page, "mouvements": page.object_list, "filtres": filtres, "types": MouvementStock.Type.choices,
        "categories": CategoriePiece.choices, "entrees": entrees, "sorties": abs(sorties),
        "variation": entrees + sorties, "params": params.urlencode(),
    })


# ---------------------------------------------------------------- inventaires
@never_cache
@login_required
def inventaires_view(request):
    if not _peut(request.user, ROLES_STOCK):
        return _refuser(request)
    form = InventaireForm(request.POST or None, initial={"date": timezone.localdate()})
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            inv = form.save(commit=False)
            inv.societe = request.user.societe
            inv.utilisateur = request.user
            inv.save()
            pieces = _pieces(request).filter(actif=True)
            if inv.categorie:
                pieces = pieces.filter(categorie=inv.categorie)
            LigneInventaire.objects.bulk_create([
                LigneInventaire(inventaire=inv, piece=p, stock_theorique=p.quantite_stock) for p in pieces
            ])
        messages.success(request, _("Inventaire créé : comptez les pièces puis clôturez."))
        return redirect("piece:inventaire_detail", pk=inv.pk)
    inventaires = InventaireStock.objects.filter(societe=request.user.societe).select_related("utilisateur")
    return render(request, "piece/stock/inventaires.html", {"form": form, "inventaires": inventaires})


@never_cache
@login_required
def inventaire_detail_view(request, pk):
    if not _peut(request.user, ROLES_STOCK):
        return _refuser(request)
    inv = get_object_or_404(InventaireStock, pk=pk, societe=request.user.societe)
    lignes = inv.lignes.select_related("piece", "piece__fabricant").order_by("piece__categorie", "piece__designation")
    en_cours = inv.statut == InventaireStock.Statut.EN_COURS

    if request.method == "POST" and en_cours:
        for ligne in lignes:
            brut = (request.POST.get(f"q_{ligne.pk}") or "").strip().replace(",", ".")
            try:
                valeur = Decimal(brut) if brut else None
            except Exception:
                continue
            if valeur != ligne.quantite_comptee:
                ligne.quantite_comptee = valeur
                ligne.save(update_fields=["quantite_comptee"])
        if request.POST.get("action") == "cloturer":
            n = stock.cloturer_inventaire(inv, utilisateur=request.user)
            messages.success(request, _("Inventaire clôturé : %(n)s régularisation(s) de stock.") % {"n": n})
        else:
            messages.success(request, _("Comptage enregistré."))
        return redirect("piece:inventaire_detail", pk=inv.pk)

    comptees = [l for l in lignes if l.quantite_comptee is not None]
    ecart_valeur = sum(((l.ecart or 0) * (l.piece.prix_achat or 0) for l in comptees), Decimal("0"))
    return render(request, "piece/stock/inventaire_detail.html", {
        "inv": inv, "lignes": lignes, "en_cours": en_cours, "nb_comptees": len(comptees),
        "ecart_valeur": ecart_valeur,
    })


# ---------------------------------------------------------------- pièces utilisées par maintenance
def _maintenance(request, maintenance_id):
    from maintenance.models import Maintenance
    s = request.user.societe
    return get_object_or_404(
        Maintenance.objects.filter(Q(societe=s) | Q(societe__isnull=True)).select_related("voiture_exemplaire"),
        pk=maintenance_id,
    )


def _piece_depuis_formulaire(request, maintenance, cd):
    """Pièce existante (id ou OEM/EAN) ou création d'une nouvelle pièce au catalogue."""
    societe = request.user.societe
    if cd.get("piece_id"):
        p = _pieces(request).filter(pk=cd["piece_id"]).first()
        if p:
            return p, False
    code = stock.normaliser_code(cd.get("code"))
    p = stock.trouver_piece(societe, code) if code else None
    if not p and not code and cd.get("designation"):
        # Sans code : même intitulé (et même fabricant si indiqué) = pièce existante
        qs = _pieces(request).filter(designation__iexact=cd["designation"].strip())
        if cd.get("fabricant"):
            qs = qs.filter(fabricant__nom__iexact=cd["fabricant"].strip())
        p = qs.first()
    if p:
        return p, False
    # Création : un code de 8/12/13/14 chiffres est un EAN, sinon c'est l'OEM
    est_ean = code.isdigit() and len(code) in (8, 12, 13, 14)
    p = Piece.objects.create(
        societe=societe,
        designation=(cd.get("designation") or code)[:150],
        categorie=cd.get("categorie") or stock.categorie_pour_maintenance(maintenance),
        unite=cd.get("unite") or "PIECE",
        oem="" if est_ean else code,
        fabricant=stock.fabricant_par_nom(cd.get("fabricant")),
        prix_vente=cd.get("prix_unitaire") or 0,
    )
    if p.fabricant:
        p.fabricants.add(p.fabricant)
    if est_ean:
        stock.definir_eans(p, [code])
    return p, True


def _synchroniser_brouillons(maintenance):
    """Factures brouillon de la maintenance : les pièces utilisées y sont ajoutées / retirées."""
    from facture.models import Facture
    from facture.services import synchroniser_pieces_utilisees
    for facture in maintenance.factures.filter(statut=Facture.Statut.BROUILLON):
        synchroniser_pieces_utilisees(facture)


@never_cache
@login_required
def pieces_maintenance_view(request, maintenance_id):
    if not _peut(request.user, ROLES_ATELIER):
        return _refuser(request)
    maintenance = _maintenance(request, maintenance_id)
    peut_gerer = _peut(request.user, ROLES_STOCK)
    donnees = request.POST if request.POST.get("action") == "ajouter" else None
    form = PieceUtiliseeForm(donnees,
                             initial={"categorie": stock.categorie_pour_maintenance(maintenance), "quantite": 1})

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "ajouter":
            if form.is_valid():
                cd = form.cleaned_data
                with transaction.atomic():
                    piece, cree = _piece_depuis_formulaire(request, maintenance, cd)
                    prix = cd.get("prix_unitaire")
                    if prix is None:
                        prix = stock.prix_vente_effectif(piece)
                    PieceUtilisee.objects.create(
                        societe=request.user.societe, maintenance=maintenance, piece=piece,
                        quantite=cd["quantite"], prix_unitaire=prix, utilisateur=request.user,
                    )
                _synchroniser_brouillons(maintenance)
                if cree:
                    messages.info(request, _("Nouvelle pièce créée au catalogue : %(p)s") % {"p": piece})
                messages.success(request, _("Pièce ajoutée à la maintenance."))
                return redirect("piece:pieces_maintenance", maintenance_id=maintenance.pk)
        else:
            pu = get_object_or_404(PieceUtilisee, pk=request.POST.get("pu"), maintenance=maintenance)
            if action == "supprimer":
                if pu.debitee:
                    messages.error(request, _("Pièce déjà débitée du stock : annulez d'abord le débit."))
                else:
                    pu.delete()
                    messages.success(request, _("Pièce retirée de la maintenance."))
            elif action == "debiter" and peut_gerer:
                stock.debiter_piece_utilisee(pu, utilisateur=request.user)
                messages.success(request, _("Pièce débitée du stock."))
            elif action == "annuler" and peut_gerer:
                stock.annuler_debit(pu, utilisateur=request.user)
                messages.success(request, _("Débit annulé : pièce remise en stock."))
            else:
                return _refuser(request)
            _synchroniser_brouillons(maintenance)
            return redirect("piece:pieces_maintenance", maintenance_id=maintenance.pk)

    lignes = maintenance.pieces_utilisees.select_related("piece", "piece__fabricant", "facture", "mouvement")
    total = sum((l.total for l in lignes), Decimal("0"))
    return render(request, "piece/stock/pieces_maintenance.html", {
        "maintenance": maintenance, "exemplaire": maintenance.voiture_exemplaire, "form": form,
        "lignes": lignes, "total": total, "peut_gerer": peut_gerer,
        "factures": maintenance.factures.all(),
        "fabricants": Fabricant.objects.order_by("nom").values_list("nom", flat=True),
        "retour": url_sure(request.GET.get("next"), request) or url_sure(request.META.get("HTTP_REFERER"), request),
    })


# ---------------------------------------------------------------- API (scan OEM / EAN)
@login_required
def api_recherche(request):
    if not _peut(request.user, ROLES_ATELIER):
        return JsonResponse({"error": "forbidden"}, status=403)
    code = request.GET.get("code") or ""
    q = request.GET.get("q") or ""

    def serialiser(p):
        return {
            "id": str(p.pk), "designation": p.designation or str(p), "oem": p.oem, "eans": p.eans,
            "fabricant": p.nom_fabricant, "categorie": p.categorie, "unite": p.unite,
            "prix_achat": str(p.prix_achat), "prix_vente": str(p.prix_vente),
            "prix_vente_effectif": str(stock.prix_vente_effectif(p)), "stock": str(p.quantite_stock),
            "emplacement": p.emplacement_etagere or "",
        }

    if code:
        p = stock.trouver_piece(request.user.societe, code)
        return JsonResponse({"found": bool(p), "piece": serialiser(p) if p else None})
    return JsonResponse({"results": [serialiser(p) for p in stock.rechercher(request.user.societe, q, 15)]})


def _maintenance_depuis_chemin(request, chemin):
    """Retrouve la maintenance d'une page de modification d'intervention à partir de son URL."""
    from django.apps import apps
    from django.urls import resolve
    try:
        match = resolve(chemin, urlconf=getattr(request, "urlconf", None))
    except Exception:
        return None
    module = getattr(match.func, "__module__", "") or ""
    app = next((c for c in sorted(apps.get_app_configs(), key=lambda c: -len(c.name))
                if module == c.name or module.startswith(c.name + ".")), None)
    if app is None:
        return None
    valeurs = [v for v in match.kwargs.values() if v]
    for modele in app.get_models():
        if not any(f.name == "maintenance" for f in modele._meta.fields):
            continue
        for v in valeurs:
            try:
                obj = modele.objects.filter(pk=v).only("maintenance").first()
            except Exception:
                continue
            if obj and obj.maintenance_id:
                return obj.maintenance_id
    return None


@login_required
def api_codes_intervention(request):
    """Codes OEM / EAN déjà enregistrés pour les lignes de pièces de l'intervention affichée (pré-remplissage)."""
    if not _peut(request.user, ROLES_ATELIER):
        return JsonResponse({"error": "forbidden"}, status=403)
    maintenance_id = _maintenance_depuis_chemin(request, request.GET.get("chemin") or "")
    if not maintenance_id:
        return JsonResponse({"lignes": {}})
    maintenance = _maintenance(request, maintenance_id)
    lignes = {}
    for pu in maintenance.pieces_utilisees.exclude(prefixe="").select_related("piece"):
        p = pu.piece
        lignes[pu.prefixe] = {
            "code": p.oem or (p.eans[0] if p.eans else ""), "designation": p.designation or str(p),
            "debitee": pu.debitee, "stock": str(p.quantite_stock),
        }
    return JsonResponse({"lignes": lignes})
