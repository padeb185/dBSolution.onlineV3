"""
Instructeurs indépendants : profils, factures d'achat et autofacturation.

L'instructeur indépendant facture ses heures à l'entreprise. Avec un accord écrit,
l'entreprise peut établir la facture au nom et pour le compte de l'instructeur
(autofacturation) : série de numéros distincte par instructeur, mention « Autofacture ».
"""
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .forms_instructeur import FactureInstructeurForm, PaiementFactureInstructeurForm, ProfilInstructeurForm
from .models import (FactureInstructeur, LigneFactureInstructeur, ProfilInstructeur, RegimeTVAInstructeur)
from .views import _autorise, _log, _refus

ROLES_INSTRUCTEUR_INDEPENDANT = ("instructeur externe",)
ZERO = Decimal("0.00")
NB_LIGNES_LIBRES = 3


def _dec(valeur, defaut=ZERO):
    try:
        return Decimal(str(valeur).replace(",", ".")) if valeur not in (None, "") else defaut
    except (InvalidOperation, ValueError):
        return defaut


def _instructeurs(request):
    from utilisateurs.models import Utilisateur
    societe = request.user.societe
    return (Utilisateur.objects.filter(societe=societe)
            .filter(Q(role__in=ROLES_INSTRUCTEUR_INDEPENDANT) | Q(profil_instructeur__isnull=False))
            .distinct().order_by("nom", "prenom"))


def _get_instructeur(request, utilisateur_id):
    return get_object_or_404(_instructeurs(request), pk=utilisateur_id)


def _factures(request):
    return FactureInstructeur.objects.filter(societe=request.user.societe).select_related("instructeur")


def _locations_non_facturees(societe, instructeur, debut=None, fin=None, facture=None):
    """Locations avec cet instructeur, pas encore reprises dans une autre facture d'instructeur."""
    from voiture.voiture_location.models import Location
    qs = Location.objects.filter(societe=societe, instructeur=instructeur, instructeur_heures__gt=0)
    if debut:
        qs = qs.filter(date_debut__gte=debut)
    if fin:
        qs = qs.filter(date_debut__lte=fin)
    deja = LigneFactureInstructeur.objects.filter(location__isnull=False)
    if facture is not None and facture.pk:
        deja = deja.exclude(facture=facture)
    return qs.exclude(pk__in=deja.values("location_id")).select_related("voiture_exemplaire").order_by("date_debut")


def _prix_defaut(profil, location):
    if profil and profil.tarif_horaire_htva is not None:
        return profil.tarif_horaire_htva
    return location.instructeur_prix_heure_htva


# ==================================================================
# INSTRUCTEURS
# ==================================================================
@never_cache
@login_required
def instructeurs_liste(request):
    if not _autorise(request.user):
        return _refus(request)

    lignes = []
    for u in _instructeurs(request):
        profil = getattr(u, "profil_instructeur", None)
        a_facturer = list(_locations_non_facturees(request.user.societe, u))
        heures = sum((Decimal(str(l.instructeur_heures or 0)) for l in a_facturer), ZERO)
        montant = sum((Decimal(str(l.instructeur_heures or 0)) * Decimal(str(_prix_defaut(profil, l) or 0))
                       for l in a_facturer), ZERO)
        factures = _factures(request).filter(instructeur=u)
        lignes.append({
            "utilisateur": u, "profil": profil,
            "nb_a_facturer": len(a_facturer), "heures_a_facturer": heures,
            "montant_a_facturer": montant.quantize(Decimal("0.01")),
            "a_payer": factures.filter(statut=FactureInstructeur.Statut.EMISE).aggregate(t=Sum("montant_tvac"))["t"] or ZERO,
        })
    return render(request, "compta/instructeurs/instructeurs_liste.html", {"lignes": lignes})


@never_cache
@login_required
def profil_instructeur(request, utilisateur_id):
    if not _autorise(request.user):
        return _refus(request)

    u = _get_instructeur(request, utilisateur_id)
    profil = getattr(u, "profil_instructeur", None)
    if request.method == "POST":
        form = ProfilInstructeurForm(request.POST, instance=profil)
        if form.is_valid():
            p = form.save(commit=False)
            p.utilisateur = u
            p.societe = request.user.societe
            p.save()
            _log(request, f"Profil instructeur indépendant – {u}")
            messages.success(request, _("Le profil de l'instructeur a été enregistré."))
            return redirect("compta:instructeurs_liste")
    else:
        form = ProfilInstructeurForm(instance=profil)
    return render(request, "compta/instructeurs/profil_form.html", {"form": form, "instructeur": u, "profil": profil})


# ==================================================================
# FACTURES
# ==================================================================
@never_cache
@login_required
def factures_instructeurs(request):
    if not _autorise(request.user):
        return _refus(request)

    factures = _factures(request)
    statut = request.GET.get("statut") or ""
    instructeur = request.GET.get("instructeur") or ""
    if statut:
        factures = factures.filter(statut=statut)
    if instructeur:
        factures = factures.filter(instructeur_id=instructeur)
    return render(request, "compta/instructeurs/factures_liste.html", {
        "factures": factures,
        "statuts": FactureInstructeur.Statut.choices,
        "instructeurs": _instructeurs(request),
        "statut": statut, "instructeur_id": instructeur,
        "total_htva": factures.aggregate(t=Sum("montant_htva"))["t"] or ZERO,
        "total_tvac": factures.aggregate(t=Sum("montant_tvac"))["t"] or ZERO,
        "total_a_payer": factures.filter(statut=FactureInstructeur.Statut.EMISE).aggregate(t=Sum("montant_tvac"))["t"] or ZERO,
    })


def _lignes_formulaire(request, profil, candidats, facture=None):
    """Lignes proposées : locations candidates (cochées si déjà dans la facture) + lignes libres."""
    existantes = {}
    libres = []
    if facture is not None and facture.pk:
        for l in facture.lignes.all():
            if l.location_id:
                existantes[l.location_id] = l
            else:
                libres.append(l)
    lignes = []
    for loc in candidats:
        l = existantes.get(loc.pk)
        lignes.append({
            "location": loc,
            "coche": bool(l) if facture is not None and facture.pk else True,
            "heures": l.heures if l else loc.instructeur_heures,
            "prix": l.prix_heure_htva if l else _prix_defaut(profil, loc),
        })
    libres_form = [{"description": l.description, "date": l.date, "heures": l.heures, "prix": l.prix_heure_htva}
                   for l in libres]
    libres_form += [{"description": "", "date": None, "heures": "", "prix": ""}] * max(0, NB_LIGNES_LIBRES - len(libres_form))
    return lignes, libres_form


def _enregistrer_lignes(request, facture, candidats):
    facture.lignes.all().delete()
    for loc in candidats:
        if request.POST.get(f"loc_{loc.pk}_inclure"):
            heures = _dec(request.POST.get(f"loc_{loc.pk}_heures"), Decimal(str(loc.instructeur_heures or 0)))
            prix = _dec(request.POST.get(f"loc_{loc.pk}_prix"))
            LigneFactureInstructeur.objects.create(
                facture=facture, location=loc, date=loc.date_debut, heures=heures, prix_heure_htva=prix,
                description=f"{_('Instruction')} – {loc.lieu} – {loc.voiture_exemplaire}"[:255],
            )
    for i in range(NB_LIGNES_LIBRES + 5):
        desc = (request.POST.get(f"libre_{i}_description") or "").strip()
        if not desc:
            continue
        d = request.POST.get(f"libre_{i}_date") or None
        LigneFactureInstructeur.objects.create(
            facture=facture, description=desc[:255], date=d,
            heures=_dec(request.POST.get(f"libre_{i}_heures"), Decimal("1")),
            prix_heure_htva=_dec(request.POST.get(f"libre_{i}_prix")),
        )
    facture.recalculer()


@never_cache
@login_required
def facture_instructeur_creer(request):
    if not _autorise(request.user):
        return _refus(request)

    societe = request.user.societe
    instructeurs = _instructeurs(request)
    instructeur_id = request.POST.get("instructeur") or request.GET.get("instructeur")
    instructeur = instructeurs.filter(pk=instructeur_id).first() if instructeur_id else None

    aujourdhui = timezone.localdate()
    premier = aujourdhui.replace(day=1)
    debut_defaut = (premier - timedelta(days=1)).replace(day=1)
    fin_defaut = premier - timedelta(days=1)

    if instructeur is None:
        return render(request, "compta/instructeurs/facture_choisir.html", {
            "instructeurs": instructeurs, "debut": debut_defaut, "fin": fin_defaut,
        })

    profil = getattr(instructeur, "profil_instructeur", None)
    if profil is None:
        messages.warning(request, _("Complétez d'abord le profil d'entreprise de l'instructeur."))
        return redirect("compta:profil_instructeur", utilisateur_id=instructeur.pk)

    facture = FactureInstructeur(societe=societe, instructeur=instructeur,
                                 regime_tva=profil.regime_tva, taux_tva=profil.taux_tva,
                                 autofacturation=profil.autofacturation_possible)
    if request.method == "POST" and "enregistrer" in request.POST:
        form = FactureInstructeurForm(request.POST, instance=facture, profil=profil)
        if form.is_valid():
            debut, fin = form.cleaned_data["periode_debut"], form.cleaned_data["periode_fin"]
            candidats = list(_locations_non_facturees(societe, instructeur, debut, fin))
            with transaction.atomic():
                facture = form.save(commit=False)
                facture.cree_par = request.user
                if not facture.date_echeance:
                    facture.date_echeance = facture.date_facture + timedelta(days=profil.delai_paiement_jours or 30)
                facture.save()
                _enregistrer_lignes(request, facture, candidats)
            if not facture.lignes.exists():
                messages.warning(request, _("Aucune ligne n'a été retenue : ajoutez des prestations."))
            _log(request, f"Création facture instructeur – {instructeur}")
            messages.success(request, _("La facture d'instructeur a été enregistrée en brouillon."))
            return redirect("compta:facture_instructeur_detail", pk=facture.pk)
        debut = form.cleaned_data.get("periode_debut") if hasattr(form, "cleaned_data") else None
        fin = form.cleaned_data.get("periode_fin") if hasattr(form, "cleaned_data") else None
    else:
        debut = _parse_date(request.GET.get("debut")) or debut_defaut
        fin = _parse_date(request.GET.get("fin")) or fin_defaut
        form = FactureInstructeurForm(instance=facture, profil=profil,
                                      initial={"periode_debut": debut, "periode_fin": fin, "date_facture": aujourdhui})

    candidats = list(_locations_non_facturees(societe, instructeur, debut, fin))
    lignes, libres = _lignes_formulaire(request, profil, candidats)
    return render(request, "compta/instructeurs/facture_form.html", {
        "form": form, "instructeur": instructeur, "profil": profil, "facture": None,
        "lignes": lignes, "libres": libres, "debut": debut, "fin": fin,
    })


def _parse_date(valeur):
    try:
        return date.fromisoformat(valeur) if valeur else None
    except ValueError:
        return None


@never_cache
@login_required
def facture_instructeur_modifier(request, pk):
    if not _autorise(request.user):
        return _refus(request)

    facture = get_object_or_404(_factures(request), pk=pk)
    if not facture.modifiable:
        messages.error(request, _("Seule une facture en brouillon peut être modifiée."))
        return redirect("compta:facture_instructeur_detail", pk=facture.pk)
    profil = facture.profil
    if request.method == "POST":
        form = FactureInstructeurForm(request.POST, instance=facture, profil=profil)
        if form.is_valid():
            debut, fin = form.cleaned_data["periode_debut"], form.cleaned_data["periode_fin"]
            candidats = list(_locations_non_facturees(facture.societe, facture.instructeur, debut, fin, facture))
            with transaction.atomic():
                facture = form.save(commit=False)
                if profil:
                    facture.regime_tva, facture.taux_tva = profil.regime_tva, profil.taux_tva
                facture.save()
                _enregistrer_lignes(request, facture, candidats)
            messages.success(request, _("La facture d'instructeur a été mise à jour."))
            return redirect("compta:facture_instructeur_detail", pk=facture.pk)
        debut, fin = facture.periode_debut, facture.periode_fin
    else:
        debut = _parse_date(request.GET.get("debut")) or facture.periode_debut
        fin = _parse_date(request.GET.get("fin")) or facture.periode_fin
        form = FactureInstructeurForm(instance=facture, profil=profil,
                                      initial={"periode_debut": debut, "periode_fin": fin})
    candidats = list(_locations_non_facturees(facture.societe, facture.instructeur, debut, fin, facture))
    lignes, libres = _lignes_formulaire(request, profil, candidats, facture)
    return render(request, "compta/instructeurs/facture_form.html", {
        "form": form, "instructeur": facture.instructeur, "profil": profil, "facture": facture,
        "lignes": lignes, "libres": libres, "debut": debut, "fin": fin,
    })


@never_cache
@login_required
def facture_instructeur_detail(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    facture = get_object_or_404(_factures(request), pk=pk)
    return render(request, "compta/instructeurs/facture_detail.html", {
        "facture": facture, "profil": facture.profil,
        "lignes": facture.lignes.select_related("location"),
        "ecritures": facture.ecritures(),
        "form_paiement": PaiementFactureInstructeurForm(
            societe=facture.societe, initial={"date_paiement": timezone.localdate()}),
    })


@login_required
@require_POST
def facture_instructeur_emettre(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    facture = get_object_or_404(_factures(request), pk=pk)
    if not facture.modifiable:
        return redirect("compta:facture_instructeur_detail", pk=facture.pk)
    if not facture.lignes.exists() or facture.montant_htva <= 0:
        messages.error(request, _("La facture ne contient aucune prestation."))
        return redirect("compta:facture_instructeur_detail", pk=facture.pk)
    if facture.autofacturation:
        profil = facture.profil
        if profil is None or not profil.autofacturation_possible:
            messages.error(request, _("Pas d'accord d'autofacturation enregistré pour cet instructeur."))
            return redirect("compta:facture_instructeur_detail", pk=facture.pk)
        with transaction.atomic():
            facture.numero = facture.prochain_numero()
            facture.statut = FactureInstructeur.Statut.EMISE
            facture.date_emission = timezone.localdate()
            facture.save()
        messages.success(request, _("Autofacture %(n)s émise. Envoyez-la à l'instructeur pour acceptation.") % {"n": facture.numero})
    else:
        if not facture.reference_instructeur:
            messages.error(request, _("Indiquez le numéro de la facture reçue de l'instructeur."))
            return redirect("compta:facture_instructeur_modifier", pk=facture.pk)
        facture.statut = FactureInstructeur.Statut.EMISE
        facture.date_emission = timezone.localdate()
        facture.save()
        messages.success(request, _("La facture de l'instructeur est enregistrée et à payer."))
    _log(request, f"Émission facture instructeur {facture.piece}")
    return redirect("compta:facture_instructeur_detail", pk=facture.pk)


@login_required
@require_POST
def facture_instructeur_payer(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    facture = get_object_or_404(_factures(request), pk=pk)
    if facture.statut == FactureInstructeur.Statut.BROUILLON:
        messages.error(request, _("Émettez d'abord la facture."))
        return redirect("compta:facture_instructeur_detail", pk=facture.pk)
    form = PaiementFactureInstructeurForm(request.POST, societe=facture.societe)
    if form.is_valid():
        facture.date_paiement = form.cleaned_data["date_paiement"]
        facture.compte_paiement = form.cleaned_data["compte_paiement"]
        facture.statut = FactureInstructeur.Statut.PAYEE
        facture.save()
        _log(request, f"Paiement facture instructeur {facture.piece}")
        messages.success(request, _("Le paiement a été enregistré."))
    else:
        messages.error(request, _("Le formulaire contient des erreurs."))
    return redirect("compta:facture_instructeur_detail", pk=facture.pk)


@login_required
@require_POST
def facture_instructeur_annuler_paiement(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    facture = get_object_or_404(_factures(request), pk=pk)
    if facture.statut == FactureInstructeur.Statut.PAYEE:
        facture.date_paiement = None
        facture.compte_paiement = None
        facture.statut = FactureInstructeur.Statut.EMISE
        facture.save()
        messages.success(request, _("Le paiement a été annulé."))
    return redirect("compta:facture_instructeur_detail", pk=facture.pk)


@never_cache
@login_required
def facture_instructeur_supprimer(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    facture = get_object_or_404(_factures(request), pk=pk)
    supprimable = facture.statut == FactureInstructeur.Statut.BROUILLON or (
        not facture.autofacturation and facture.statut != FactureInstructeur.Statut.PAYEE)
    if not supprimable:
        messages.error(request, _("Une autofacture émise ou une facture payée ne peut pas être supprimée."))
        return redirect("compta:facture_instructeur_detail", pk=facture.pk)
    if request.method == "POST":
        _log(request, f"Suppression facture instructeur {facture.piece}")
        facture.delete()
        messages.success(request, _("La facture d'instructeur a été supprimée."))
        return redirect("compta:factures_instructeurs")
    return render(request, "compta/instructeurs/facture_supprimer.html", {"facture": facture})


@never_cache
@login_required
def facture_instructeur_pdf(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    from weasyprint import HTML

    facture = get_object_or_404(_factures(request), pk=pk)
    html = render_to_string("compta/instructeurs/facture_pdf.html", {
        "facture": facture, "profil": facture.profil,
        "lignes": facture.lignes.select_related("location"),
        "societe": facture.societe, "instructeur": facture.instructeur,
        "date_export": timezone.now(),
    }, request=request)
    pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()
    nom = (_("Autofacture") if facture.autofacturation else _("Facture_instructeur"))
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{nom}_{facture.piece}.pdf"'
    return response
