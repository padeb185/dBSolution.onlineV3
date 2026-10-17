from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import  redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.cache import never_cache
from .forms import VoitureExemplaireForm, VoitureExemplaireFinanceForm, FINANCE_FIELDS
from .models import VoitureExemplaire
from ..voiture_modele.models import VoitureModele
from ..voiture_moteur.models import MoteurVoiture
from django.utils.translation import gettext as _
from ..voiture_boite.models import VoitureBoite
from ..voiture_embrayage.models import VoitureEmbrayage
from ..voiture_freins_av.models import VoitureFreinsAV
from ..voiture_freins_ar.models import VoitureFreinsAR
from ..voiture_pneus.models import VoiturePneus, TrainPneus
from ..voiture_pneus import services_trains as trains_services
from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.db.models.deletion import ProtectedError



@never_cache
@login_required
def liste_exemplaires(request, modele_id):
    modele = get_object_or_404(
        VoitureModele,
        id=modele_id,
    )

    exemplaires = (
        VoitureExemplaire.objects
        .filter(voiture_modele=modele)
        .order_by("id")
    )

    # Décomposer l'immatriculation belge (1-ABC-234)
    for ex in exemplaires:
        immat = (ex.immatriculation or "").replace("-", "").upper()

        if len(immat) == 7:
            ex.chiffre = immat[0]
            ex.lettres = immat[1:4]
            ex.chiffres = immat[4:7]
        else:
            ex.chiffre = ""
            ex.lettres = ""
            ex.chiffres = ""

    return render(
        request,
        "voiture_exemplaire/liste_exemplaires.html",
        {
            "modele": modele,
            "exemplaires": exemplaires,
        },
    )


@never_cache
@login_required
def voiture_exemplaire_detail(request, exemplaire_id):
    exemplaire = get_object_or_404(
        VoitureExemplaire,
        id=exemplaire_id,
    )

    modele = exemplaire.voiture_modele
    marque = modele.voiture_marque

    for moteur in exemplaire.moteurs.all():
        moteur.save()

    exemplaire.refresh_from_db()

    trains_services.initialiser_trains(exemplaire)
    trains_pneus = trains_services.resume_trains(exemplaire)

    return render(
        request,
        "voiture_exemplaire/detail_exemplaire.html",
        {
            "exemplaire": exemplaire,
            "modele": modele,
            "marque": marque,
            "trains_pneus": trains_pneus,
            "a_seconde_monte": any(p["autres_actifs"] or (p["train_monte"] and p["train_monte"].monte == "seconde") for p in trains_pneus),
        },
    )

@login_required
def lier_boite_exemplaire(request, exemplaire_id):
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
    boites = VoitureBoite.objects.all().order_by('fabricant')

    if request.method == "POST":
        boite_id = request.POST.get("boite_id")
        if boite_id:
            boite = get_object_or_404(VoitureBoite, id=boite_id)
            boite.voitures_exemplaires.add(exemplaire)
            messages.success(request, _(f"La boîte de vitesse a été liée au véhicule '{exemplaire.voiture_marque} { exemplaire.immatriculation}' avec succès."))


            return redirect("voiture_exemplaire:lier_boite_exemplaire", exemplaire_id=exemplaire.id)
        else:
            messages.error(request, _("Veuillez sélectionner une boîte à lier."))

    return render(request, "voiture_exemplaire/lier_boite.html", {
        "exemplaire": exemplaire,
        "boites": boites,
        "title": _("Lier une boîte de vitesse à un véhicule"),
    })




EMPLACEMENTS = VoiturePneus.EmplacementPneus


def _pneus_compatibles(request, position):
    """Pneus du catalogue de la société compatibles avec l'essieu."""
    return (
        VoiturePneus.objects
        .filter(emplacement__in=[position, EMPLACEMENTS.AVANT_ET_ARRIERE])
        .filter(Q(societe=getattr(request.user, "societe", None)) | Q(societe__isnull=True))
        .order_by("manufacturier")
    )


def _monte_demandee(request):
    monte = request.POST.get("monte") or request.GET.get("monte") or TrainPneus.Monte.PREMIERE
    return monte if monte in TrainPneus.Monte.values else TrainPneus.Monte.PREMIERE


def _lier_pneus(request, exemplaire_id, emplacement, url_name, titre):
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
    monte = _monte_demandee(request)
    pneus = _pneus_compatibles(request, emplacement)

    trains_services.initialiser_trains(exemplaire)

    if request.method == "POST":
        pneu_id = request.POST.get("pneu_id")

        if pneu_id:
            pneu = get_object_or_404(pneus, id=pneu_id)
            trains_services.lier_pneus(exemplaire, emplacement, monte, pneu)

            messages.success(
                request,
                _("Les pneus (%(monte)s) ont été liés au véhicule « %(vehicule)s » avec succès.") % {
                    "monte": TrainPneus.Monte(monte).label,
                    "vehicule": f"{exemplaire.voiture_marque} {exemplaire.immatriculation}",
                },
            )
            return redirect(f"{reverse(url_name, kwargs={'exemplaire_id': exemplaire.id})}?monte={monte}")

        messages.error(request, _("Veuillez sélectionner des pneus à lier."))

    train = trains_services.train_actif(exemplaire, emplacement, monte)
    pneu_actuel = train.voiture_pneus if train else None

    return render(
        request,
        "voiture_exemplaire/lier_pneus.html",
        {
            "exemplaire": exemplaire,
            "pneus": pneus,
            "title": titre,
            "emplacement": emplacement,  # "avant" ou "arriere"
            "monte": monte,              # "premiere" ou "seconde"
            "montes": TrainPneus.Monte.choices,
            "train": train,
            "pneu_actuel": pneu_actuel,
        },
    )


@login_required
def lier_pneus_av(request, exemplaire_id):
    return _lier_pneus(
        request,
        exemplaire_id,
        emplacement=EMPLACEMENTS.AVANT,
        url_name="voiture_exemplaire:lier_pneus_av",
        titre=_("Lier des pneus avant à un véhicule"),
    )


@login_required
def lier_pneus_ar(request, exemplaire_id):
    return _lier_pneus(
        request,
        exemplaire_id,
        emplacement=EMPLACEMENTS.ARRIERE,
        url_name="voiture_exemplaire:lier_pneus_ar",
        titre=_("Lier des pneus arrière à un véhicule"),
    )


def _entier_positif(valeur, defaut):
    try:
        valeur = int(str(valeur).replace(" ", "").replace(".", ""))
    except (TypeError, ValueError):
        return defaut
    return valeur if valeur >= 0 else defaut


@login_required
def remplacer_train_pneus(request, exemplaire_id, position):
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
    if position not in TrainPneus.Position.values:
        return redirect("voiture_exemplaire:voiture_exemplaire_detail", exemplaire_id=exemplaire.id)

    trains_services.initialiser_trains(exemplaire)
    monte = _monte_demandee(request)
    pneus = _pneus_compatibles(request, position)
    km_actuel = exemplaire.kilometres_chassis or 0
    train = trains_services.train_actif(exemplaire, position, monte)

    if request.method == "POST":
        pneu_id = request.POST.get("pneu_id")
        km = _entier_positif(request.POST.get("km_chassis"), km_actuel)
        date = parse_date(request.POST.get("date_remplacement") or "") or timezone.localdate()

        erreurs = []
        if not pneu_id:
            erreurs.append(_("Veuillez sélectionner les nouveaux pneus."))
        if km < km_actuel:
            erreurs.append(
                _("Le kilométrage (%(km)s) ne peut pas être inférieur au kilométrage actuel du véhicule (%(actuel)s).")
                % {"km": km, "actuel": km_actuel}
            )

        if not erreurs:
            pneu = get_object_or_404(pneus, id=pneu_id)
            ancien, nouveau = trains_services.remplacer_train(exemplaire, position, monte, pneu, km, date)
            if ancien:
                messages.success(
                    request,
                    _("Train n°%(ancien)s archivé (%(km)s km). Nouveau train n°%(nouveau)s installé à 0 km.")
                    % {"ancien": ancien.numero, "km": ancien.km_effectues, "nouveau": nouveau.numero},
                )
            else:
                messages.success(
                    request,
                    _("Train n°%(nouveau)s installé.") % {"nouveau": nouveau.numero},
                )
            return redirect("voiture_exemplaire:voiture_exemplaire_detail", exemplaire_id=exemplaire.id)

        for erreur in erreurs:
            messages.error(request, erreur)

    return render(
        request,
        "voiture_exemplaire/remplacer_train_pneus.html",
        {
            "exemplaire": exemplaire,
            "position": position,
            "position_label": TrainPneus.Position(position).label,
            "monte": monte,
            "montes": TrainPneus.Monte.choices,
            "train": train,
            "pneus": pneus,
            "km_actuel": km_actuel,
            "aujourdhui": timezone.localdate(),
        },
    )


@login_required
def basculer_monte_pneus(request, exemplaire_id):
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
    if request.method != "POST":
        return redirect("voiture_exemplaire:voiture_exemplaire_detail", exemplaire_id=exemplaire.id)

    km_actuel = exemplaire.kilometres_chassis or 0
    km = _entier_positif(request.POST.get("km_chassis"), km_actuel)
    if km < km_actuel:
        messages.error(
            request,
            _("Le kilométrage (%(km)s) ne peut pas être inférieur au kilométrage actuel du véhicule (%(actuel)s).")
            % {"km": km, "actuel": km_actuel},
        )
    else:
        nb = trains_services.basculer_monte(exemplaire, km)
        if nb:
            messages.success(request, _("Monte basculée (première ↔ seconde) au kilométrage %(km)s.") % {"km": km})
        else:
            messages.error(request, _("Aucune seconde monte n'est enregistrée pour ce véhicule."))

    return redirect("voiture_exemplaire:voiture_exemplaire_detail", exemplaire_id=exemplaire.id)





@login_required
def lier_moteur_exemplaire(request, exemplaire_id):
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
    moteurs = MoteurVoiture.objects.all().order_by('motoriste')

    if request.method == "POST":
        moteur_id = request.POST.get("moteur_id")
        if moteur_id:
            moteur = get_object_or_404(MoteurVoiture, id=moteur_id)
            moteur.voitures_exemplaires.add(exemplaire)
            messages.success(request, _(f"Le moteur a été lié au véhicule '{exemplaire.voiture_marque} { exemplaire.immatriculation }' avec succès."))


            return redirect("voiture_exemplaire:lier_moteur_exemplaire", exemplaire_id=exemplaire.id)
        else:
            messages.error(request, _("Veuillez sélectionner un moteur à lier."))

    return render(request, "voiture_exemplaire/lier_moteur.html", {
        "exemplaire": exemplaire,
        "moteurs": moteurs,
        "title": _("Lier un moteur à un véhicule"),
    })



@login_required
def lier_embrayage_exemplaire(request, exemplaire_id):
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
    embrayages = VoitureEmbrayage.objects.all().order_by('fabricant')

    if request.method == "POST":
        embrayage_id = request.POST.get("embrayage_id")
        if embrayage_id:
            embrayage = get_object_or_404(VoitureEmbrayage, id=embrayage_id)
            embrayage.voitures_exemplaires.add(exemplaire)
            messages.success(request, _(f"L'embrayage a été lié au véhicule '{exemplaire.voiture_marque} { exemplaire.immatriculation }' avec succès."))


            return redirect("voiture_exemplaire:lier_embrayage_exemplaire", exemplaire_id=exemplaire.id)
        else:
            messages.error(request, _("Veuillez sélectionner un embrayage à lier."))

    return render(request, "voiture_exemplaire/lier_embrayage.html", {
        "exemplaire": exemplaire,
        "embrayages": embrayages,
        "title": _("Lier un embrayage à un véhicule"),
    })



@login_required
def lier_freins(request, exemplaire_id):
    exemplaire = get_object_or_404(
        VoitureExemplaire,
        id=exemplaire_id
    )

    freins = VoitureFreinsAV.objects.all().order_by("taille_disque_av")

    if request.method == "POST":
        frein_id = request.POST.get("frein_id")
        marque_disques_av = request.POST.get("marque_disques_av")
        marque_plaquettes_av = request.POST.get("marque_plaquettes_av")

        if not frein_id:
            messages.error(
                request,
                _("Veuillez sélectionner un système de freinage à lier.")
            )
            return redirect(
                "voiture_exemplaire:lier_frein",
                exemplaire_id=exemplaire.id
            )

        frein = get_object_or_404(
            VoitureFreinsAV,
            id=frein_id
        )

        if marque_disques_av:
            frein.marque_disques_av = marque_disques_av

        if marque_plaquettes_av:
            frein.marque_plaquettes_av = marque_plaquettes_av

        frein.save()

        frein.voitures_exemplaires.add(exemplaire)

        messages.success(
            request,
            _(
                f"Le système de freinage avant a été lié au véhicule "
                f"'{exemplaire.voiture_marque} {exemplaire.immatriculation}' avec succès."
            )
        )

        return redirect(
            "voiture_exemplaire:lier_frein",
            exemplaire_id=exemplaire.id
        )

    return render(request, "voiture_exemplaire/lier_frein.html", {
        "exemplaire": exemplaire,
         "freins": freins,
        "title": _("Lier un système de freinage avant à un véhicule"),
    })




@login_required
def lier_frein_ar(request, exemplaire_id):

    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    freins_ar = VoitureFreinsAR.objects.all().order_by('taille_disque_ar')
    marque_disques_ar = request.POST.get("marque_disques_ar")
    marque_plaquettes_ar = request.POST.get("marque_plaquettes_ar")

    if request.method == "POST":
        frein_ar_id = request.POST.get("frein_ar_id")
        if frein_ar_id:
            frein_ar = get_object_or_404(VoitureFreinsAR, id=frein_ar_id)

            if marque_disques_ar:
                frein_ar.marque_disques_av = marque_disques_ar
            if marque_plaquettes_ar:
                frein_ar.marque_plaquettes_av = marque_plaquettes_ar
            frein_ar.save()

                # Lier le frein à l'exemplaire
            frein_ar.voitures_exemplaires.add(exemplaire)
            messages.success(request, _(f"Le système de freinage arrière a été lié au véhicule '{exemplaire.voiture_marque}  { exemplaire.immatriculation }' avec succès."))

                # Redirection vers la page de détail de l'exemplaire (ou une page liste)
            return redirect("voiture_exemplaire:lier_frein_ar", exemplaire_id=exemplaire.id)
        else:
            messages.error(request, _("Veuillez sélectionner un système de freinage à lier."))

    return render(request, "voiture_exemplaire/lier_frein_ar.html", {
        "exemplaire": exemplaire,
        "freins_ar": freins_ar,
        "title": _("Lier un système de freinage arrière à un véhicule"),
    })







@login_required
def moteur_autocomplete(request):

    code = request.GET.get("code_moteur")
    motoriste = request.GET.get("motoriste")

    if not code or not motoriste:
        return JsonResponse({"error": _("Paramètres manquants")}, status=400)


    moteur = MoteurVoiture.objects.filter(code_moteur=code, motoriste=motoriste).first()
    if not moteur:
        return JsonResponse({"error": _("Moteur non trouvé")}, status=404)

    # Retourne les champs à remplir
    data = {
        "type_moteur": moteur.type_moteur,
        "carburant": moteur.carburant,
        "cylindree_l": moteur.cylindree_l,
        "distribution": moteur.distribution,
        "nombre_cylindres": moteur.nombre_cylindres,
        "puissance_ch": moteur.puissance_ch,
        "puissance_tr_min": moteur.puissance_tr_min,
        "couple_nm": moteur.couple_nm,
        "couple_tr_min": moteur.couple_tr_min,
        "qualite_huile": moteur.qualite_huile,
        "quantite_huile_l": moteur.quantite_huile_l,
        "intervalle_km_entretien": moteur.intervalle_km_entretien,
    }

    return JsonResponse(data)



@login_required
def modifier_exemplaire(request, exemplaire_id):
    tenant = request.user.societe

    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    if request.method == "POST":
        form = VoitureExemplaireForm(
            request.POST,
            instance=exemplaire,
            user=request.user
        )

        if form.is_valid():
            exemplaire = form.save(commit=False)
            exemplaire.societe = tenant
            exemplaire.save()

            messages.success(
                request,
                _("Véhicule '%(vehicule)s' mis à jour avec succès.") % {
                    "vehicule": f"{exemplaire.voiture_marque} {exemplaire.immatriculation}"
                }
            )

            return redirect(
                f"{reverse('voiture_exemplaire:voiture_exemplaire_detail', kwargs={'exemplaire_id': exemplaire.id})}?saved=1"
            )

    else:
        form = VoitureExemplaireForm(
            instance=exemplaire,
            user=request.user
       )

    return render(request, "voiture_exemplaire/modifier_exemplaire.html", {
        "form": form,
        "exemplaire": exemplaire,
    })


    
@never_cache
@login_required
def liste_exemplaires_all(request):

    exemplaires = VoitureExemplaire.objects.select_related(
            'voiture_marque', 'voiture_modele'  # Ce sont les bons noms de champs
        ).all().order_by('id')

    return render(
        request,
        'voiture_exemplaire/list.html',
        {
            'exemplaires': exemplaires
        }
    )


@login_required
def ajouter_exemplaire_all(request, modele_id):

    modele = get_object_or_404(
        VoitureModele,
        id=modele_id
    )
    marque = modele.voiture_marque

    if request.method == "POST":
        form = VoitureExemplaireForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():
            instance = form.save(commit=False)

            annee = form.cleaned_data.get("annee_production")

            instance.voiture_modele = modele
            instance.voiture_marque = marque
            instance.societe = request.user.societe
            instance.est_apres_2010 = bool(
                annee and annee > 2010
            )

            instance.save()

            messages.success(
                request,
                _("Véhicule '%(vehicule)s' créé avec succès.") % {
                    "vehicule": (
                        f"{instance.voiture_marque} "
                        f"{instance.immatriculation}"
                    )
                }
            )


            return redirect(
                f"{reverse('voiture_exemplaire:voiture_exemplaire', kwargs={'modele_id': modele.id})}?saved=1"
            )

    else:
        form = VoitureExemplaireForm(
            user=request.user,
            initial={
                "voiture_marque": marque,
                "voiture_modele": modele,
            }
        )

    return render(
        request,
        "voiture_exemplaire/ajouter_exemplaire_all.html",
        {
            "form": form,
            "modele": modele,
            "marque": marque,
        }
    )




@login_required
def supprimer_exemplaire_all(request, exemplaire_id):

    # ==========================================================
    # RÉCUPÉRATION DU VÉHICULE
    # ==========================================================
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.select_related(
            "voiture_modele",
            "voiture_marque",
            "societe",
        ),
        id=exemplaire_id,
    )

    modele = exemplaire.voiture_modele
    marque = exemplaire.voiture_marque

    # ==========================================================
    # SÉCURITÉ TENANT
    # ==========================================================
    if exemplaire.societe != request.user.societe:
        messages.error(
            request,
            _("Accès refusé")
        )
        return redirect(
            "utilisateurs:dashboard"
        )

    # ==========================================================
    # AUTORISATIONS
    # ==========================================================
    roles_autorises = [
        "direction",
        "chef_mecanicien",
    ]

    if (
        request.user.role not in roles_autorises
        and not request.user.is_superuser
    ):
        messages.error(
            request,
            _("Accès refusé")
        )
        return redirect(
            "utilisateurs:dashboard"
        )

    # ==========================================================
    # SUPPRESSION
    # ==========================================================
    if request.method == "POST":

        try:
            exemplaire.delete()

            messages.success(
                request,
                _("Véhicule '%(vehicule)s' supprimé avec succès.") % {
                    "vehicule": (
                        f"{marque} "
                        f"{exemplaire.immatriculation}"
                    )
                }
            )

        except ProtectedError:
            messages.error(
                request,
                _(
                    "Impossible de supprimer ce véhicule car "
                    "des données lui sont encore associées."
                )
            )
        return redirect(
            f"{reverse('voiture_exemplaire:list')}?deleted=1"
        )

    # ==========================================================
    # PAGE DE CONFIRMATION
    # ==========================================================
    return render(
        request,
        "voiture_exemplaire/supprimer_exemplaire_all.html",
        {
            "exemplaire": exemplaire,
            "modele": modele,
            "marque": marque,
        }
    )


# =====================================================================
# DONNÉES FINANCIÈRES — CRUD (onglet Direction)
# =====================================================================

FINANCE_ROLES = ["direction"]


def _finance_autorise(user):
    return user.is_superuser or getattr(user, "role", None) in FINANCE_ROLES


def _finance_manquants(exemplaire):
    """Liste des champs financiers encore vides."""
    return [f for f in FINANCE_FIELDS if getattr(exemplaire, f) is None]


def _finance_queryset(request):
    return (
        VoitureExemplaire.objects
        .select_related("voiture_marque", "voiture_modele", "client")
        .filter(societe=request.user.societe)
    )


def _police_active(exemplaire):
    """Police d'assurance active liée au véhicule (si l'app est utilisée)."""
    polices = getattr(exemplaire, "polices_assurance", None)
    if polices is None:
        return None
    return polices.filter(actif=True).order_by("-date_debut").first()


@never_cache
@login_required
def finances_liste(request):
    if not _finance_autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    filtre = request.GET.get("filtre", "tous")
    q = (request.GET.get("q") or "").strip()

    exemplaires = _finance_queryset(request).order_by(
        "voiture_marque__nom_marque", "voiture_modele__nom_modele", "immatriculation"
    )

    if q:
        from django.db.models import Q
        exemplaires = exemplaires.filter(
            Q(immatriculation__icontains=q)
            | Q(numero_vin__icontains=q)
            | Q(voiture_marque__nom_marque__icontains=q)
            | Q(voiture_modele__nom_modele__icontains=q)
        )

    lignes = []
    nb_complets = 0
    for ex in exemplaires:
        manquants = _finance_manquants(ex)
        complet = not manquants
        nb_complets += complet
        if filtre == "incomplets" and complet:
            continue
        if filtre == "complets" and not complet:
            continue
        ex.nb_manquants = len(manquants)
        ex.cout_fixe_annuel = (ex.assurance or 0) + (ex.taxe_roulage or 0)
        lignes.append(ex)

    total = exemplaires.count()

    return render(request, "voiture_exemplaire/finances/liste.html", {
        "exemplaires": lignes,
        "filtre": filtre,
        "q": q,
        "total": total,
        "nb_complets": nb_complets,
        "nb_incomplets": total - nb_complets,
        "nb_champs": len(FINANCE_FIELDS),
    })


@never_cache
@login_required
def finances_detail(request, exemplaire_id):
    if not _finance_autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    exemplaire = get_object_or_404(_finance_queryset(request), id=exemplaire_id)
    manquants = _finance_manquants(exemplaire)

    labels = VoitureExemplaireFinanceForm().fields
    champs = []
    for f in FINANCE_FIELDS:
        valeur = getattr(exemplaire, f)
        if f == "etat_achat" and valeur is not None:
            valeur = exemplaire.get_etat_achat_display()
        elif f == "kilometrage_achat" and valeur is not None:
            valeur = f"{valeur} km"
        champs.append({"nom": f, "label": labels[f].label, "valeur": valeur})

    # Entretien interne : factures à notre propre société pour ce véhicule (coût de revient HTVA)
    from decimal import Decimal
    from facture.models import Facture
    entretiens = []
    total_entretien = Decimal("0.00")
    for f in (
        Facture.objects.filter(voiture_exemplaire=exemplaire, client_est_societe=True, statut=Facture.Statut.EMISE)
        .prefetch_related("lines").order_by("-issue_date")
    ):
        c = f.couts_internes()
        entretiens.append({"facture": f, **c})
        total_entretien += c["total"]

    return render(request, "voiture_exemplaire/finances/detail.html", {
        "entretiens": entretiens,
        "total_entretien": total_entretien,
        "exemplaire": exemplaire,
        "champs": champs,
        "manquants": manquants,
        "police": _police_active(exemplaire),
        "cout_fixe_annuel": (exemplaire.assurance or 0) + (exemplaire.taxe_roulage or 0),
        "cout_acquisition": (exemplaire.prix_achat or 0) + (exemplaire.taxe_mise_en_circulation or 0),
    })


@login_required
def finances_modifier(request, exemplaire_id):
    """Création (compléter les champs vides) et modification des données financières."""
    if not _finance_autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    exemplaire = get_object_or_404(_finance_queryset(request), id=exemplaire_id)
    police = _police_active(exemplaire)

    if request.method == "POST":
        form = VoitureExemplaireFinanceForm(request.POST, instance=exemplaire)
        if form.is_valid():
            from django.utils import timezone
            # update() : n'écrit que les champs financiers, sans relancer
            # le décodage VIN ni le recalcul des kilométrages de save().
            VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
                updated_at=timezone.now(),
                **{f: form.cleaned_data.get(f) for f in FINANCE_FIELDS},
            )
            messages.success(
                request,
                _("Données financières de '%(vehicule)s' enregistrées.") % {
                    "vehicule": f"{exemplaire.voiture_marque} {exemplaire.immatriculation}"
                },
            )
            return redirect("voiture_exemplaire:finances_detail", exemplaire_id=exemplaire.id)
    else:
        initial = {}
        # Pré-remplissage de l'assurance depuis la police active si vide
        if exemplaire.assurance is None and police and police.prime_annuelle is not None:
            initial["assurance"] = police.prime_annuelle
        form = VoitureExemplaireFinanceForm(instance=exemplaire, initial=initial)

    return render(request, "voiture_exemplaire/finances/form.html", {
        "form": form,
        "exemplaire": exemplaire,
        "police": police,
        "manquants": _finance_manquants(exemplaire),
    })


@login_required
def finances_supprimer(request, exemplaire_id):
    """Efface les données financières (le véhicule lui-même est conservé)."""
    if not _finance_autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    exemplaire = get_object_or_404(_finance_queryset(request), id=exemplaire_id)

    if request.method == "POST":
        from django.utils import timezone
        VoitureExemplaire.objects.filter(pk=exemplaire.pk).update(
            updated_at=timezone.now(),
            **{f: None for f in FINANCE_FIELDS},
        )
        messages.success(
            request,
            _("Données financières de '%(vehicule)s' supprimées.") % {
                "vehicule": f"{exemplaire.voiture_marque} {exemplaire.immatriculation}"
            },
        )
        return redirect("voiture_exemplaire:finances_liste")

    return render(request, "voiture_exemplaire/finances/supprimer.html", {
        "exemplaire": exemplaire,
    })
