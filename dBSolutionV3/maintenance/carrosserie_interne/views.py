from django.template.loader import render_to_string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models, transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, CreateView
from django_tenants.utils import tenant_context
from utilisateurs.models import UserLog
from weasyprint import HTML
from .forms import CarrosserieInterneForm
from .models import CarrosserieInterne
from carrosserie.models import Carrosserie
from voiture.voiture_exemplaire.models import VoitureExemplaire
from maintenance.models import Maintenance
from utilisateurs.apprentis.models import Apprenti
from utilisateurs.chef_mecanicien.models import ChefMecanicien
from utilisateurs.direction.models import Direction
from utilisateurs.magasinier.models import Magasinier
from utilisateurs.mecanicien.models import Mecanicien





@method_decorator([login_required, never_cache], name='dispatch')
class CarrosserieInterneListView(LoginRequiredMixin, ListView):
    model = CarrosserieInterne
    template_name = "carrosserie_interne/carrosserie_interne_list.html"
    context_object_name = "carrosserie_internes"
    paginate_by = 20
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = CarrosserieInterne.objects.select_related(
            "voiture_exemplaire",
            "societe",
            "tech_technicien",
            "tech_societe",
        )

        # 🔥 filtre par exemplaire (IMPORTANT)
        exemplaire_id = self.kwargs.get("exemplaire_id")
        if exemplaire_id:
            queryset = queryset.filter(voiture_exemplaire_id=exemplaire_id)

        # 🔥 filtre par société
        societe = getattr(self.request.user, "societe", None)
        if societe:
            queryset = queryset.filter(
                models.Q(societe=societe) | models.Q(societe__isnull=True)
            )

        return queryset.order_by(*self.ordering)

    from django.shortcuts import get_object_or_404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exemplaire_id = self.kwargs.get("exemplaire_id")
        context["exemplaire"] = get_object_or_404(
            VoitureExemplaire,
            id=exemplaire_id
        )

        context["is_checkup_allowed"] = self.request.user.role in [
            "direction",
            "mecanicien",
            "chef_mecanicien",
            "magasinier",
        ]



        # Structuration des champs du formulaire en sections
        form = context.get("form")
        if form:
            context["sections"] = [
                {
                    "title": "Kilométrage",
                    "icon": "icons/compteur.png",
                    "fields": [f for f in form if "kilo" in f.name],
                },
                {
                    "title": "Pare-chocs",
                    "icon": "icons/pare-chocs.png",
                    "fields": [f for f in form if "pare" in f.name],
                },
                {
                    "title": "Traverse",
                    "icon": "icons/pare-chocs.png",
                    "fields": [f for f in form if "bouclier" in f.name],
                },
                {
                    "title": "Etiquette",
                    "icon": "icons/tag.png",
                    "fields": [f for f in form if "tag" in f.name],
                },
                {
                    "title": "Remarques",
                    "icon": "icons/notes.png",
                    "fields": [f for f in form if "remarques" in f.name],
                },
                {
                    "title": "Technicien",
                    "icon": "icons/mecanicien.png",
                    "fields": [f for f in form if "tech" in f.name],
                },
            ]
        else:
            context["sections"] = []

        return context



@never_cache
@login_required
def carrosserie_interne_create_view(request, exemplaire_id):

    tenant = request.user.societe
    role = request.user.role

    with tenant_context(tenant):

        # 🔎 Récupération exemplaire
        exemplaire = get_object_or_404(
            VoitureExemplaire.objects.filter(
                Q(client__societe=tenant) |
                Q(client__isnull=True, societe=tenant)
            ),
            id=exemplaire_id
        )

        # 🔐 Vérification rôles
        roles_autorises = [
            "mecanicien",
            "apprenti",
            "magasinier",
            "chef_mecanicien",
            "direction"
        ]

        if role not in roles_autorises:
            messages.error(request, _("Accès refusé"))
            return redirect("utilisateurs:dashboard")

        # =========================
        # POST
        # =========================

        maintenance = None

        if request.method == "POST":

            form = CarrosserieInterneForm(
                request.POST,
                user=request.user,
                exemplaire=exemplaire
            )

            if form.is_valid():

                try:
                    with transaction.atomic():

                        km = form.cleaned_data.get("kilometrage_intervention")

                        # 🔗 Création objet AVANT tout traitement
                        carrosserie_interne = form.save(commit=False)

                        # ✅ Relations obligatoires AVANT assign_technicien/save
                        carrosserie_interne.societe = tenant
                        carrosserie_interne.voiture_exemplaire = exemplaire
                        carrosserie_interne.tech_last_maintained_by = request.user

                        if km is not None:
                            km = int(km)

                            ancien_km = exemplaire.kilometres_chassis

                            if km < ancien_km:
                                form.add_error(
                                    "kilometrage_intervention",
                                    _("Le kilométrage ne peut pas diminuer.")
                                )
                                raise ValueError("Kilométrage invalide")

                            exemplaire.kilometres_chassis = km
                            exemplaire.date_derniere_intervention = timezone.now().date()
                            exemplaire.update_kilometres()
                            exemplaire.save()

                            carrosserie_interne.kilometres_chassis = exemplaire.kilometres_chassis
                            carrosserie_interne.kilometrage_intervention = km
                        else:
                            carrosserie_interne.kilometres_chassis = exemplaire.kilometres_chassis

                        carrosserie_interne.assign_technicien(request.user)

                        maintenance = Maintenance.objects.create(
                            societe=tenant,
                            voiture_exemplaire=exemplaire,
                            immatriculation=exemplaire.immatriculation,
                            date_intervention=timezone.now().date(),
                            kilometres_chassis=exemplaire.kilometres_chassis,
                            kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                            type_maintenance=Maintenance.TypeMaintenance.CARROSSERIE_INTERNE,
                            tag=Maintenance.Tag.JAUNE,
                        )

                        if role == "mecanicien":
                            maintenance.mecanicien = Mecanicien.objects.get(id=request.user.id)
                        elif role == "chef_mecanicien":
                            maintenance.chef_mecanicien = ChefMecanicien.objects.get(id=request.user.id)
                        elif role == "apprenti":
                            maintenance.apprentis = Apprenti.objects.get(id=request.user.id)
                        elif role == "magasinier":
                            maintenance.magasinier = Magasinier.objects.get(id=request.user.id)
                        elif role == "direction":
                            maintenance.direction = Direction.objects.get(id=request.user.id)

                        maintenance.save()

                        carrosserie_interne.maintenance = maintenance
                        carrosserie_interne.save()

                        UserLog.objects.create(
                            utilisateur=request.user,
                            action=_("Carrosserie  - %(immatriculation)s") % {
                                "immatriculation": exemplaire.immatriculation
                            }
                        )

                    messages.success(request, _("Intervention carrosserie enregistrée avec succès."))

                except Exception as e:
                    messages.error(request, _(f"Erreur : {str(e)}"))
            else:
                print("FORM INVALID:", form.errors)
                messages.error(request, _("Le formulaire contient des erreurs."))

        carrosserie_interne = CarrosserieInterne(
            societe=tenant,
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis

        )

        carrosserie_interne.assign_technicien(request.user)

        form = CarrosserieInterneForm(
            instance=carrosserie_interne,
            user=request.user,
            exemplaire=exemplaire

        )

        # 🔥 SECTIONS (remplace ton get_context_data)
        sections = [
            {
                "title": "Kilométrage",
                "icon": "icons/compteur.png",
                "fields": [f for f in form if "kilo" in f.name],
            },
            {
                "title": "Pare-chocs avant",
                "icon": "icons/pare-chocs.png",
                "fields": [f for f in form if "pare_choc_av" in f.name],
            },
            {
                "title": "Pare-chocs arrière",
                "icon": "icons/pare-chocs.png",
                "fields": [f for f in form if "pare_choc_ar" in f.name],
            },
            {
                "title": "Traverse avant",
                "icon": "icons/pare-chocs.png",
                "fields": [f for f in form if "bouclier_av" in f.name],
            },
            {
                "title": "Traverse arrière",
                "icon": "icons/pare-chocs.png",
                "fields": [f for f in form if "bouclier_ar" in f.name],
            },

            {
                "title": "Support pare-chocs avant",
                "icon": "icons/pare-chocs.png",
                "fields": [f for f in form if "support_pa_choc_av" in f.name],
            },
            {
                "title": "Support pare-chocs arrière",
                "icon": "icons/pare-chocs.png",
                "fields": [f for f in form if "support_pa_choc_ar" in f.name],
            },

            {
                "title": "Calandre",
                "icon": "icons/calandre.png",
                "fields": [f for f in form if "calandre" in f.name],
            },
            {
                "title": "Aile avant droite",
                "icon": "icons/aile.png",
                "fields": [f for f in form if "aile_avd" in f.name],
            },

            {
                "title": "Aile avant gauche",
                "icon": "icons/aile.png",
                "fields": [f for f in form if "aile_avg" in f.name],
            },
            {
                "title": "Aile arrière droite",
                "icon": "icons/aile_ar.png",
                "fields": [f for f in form if "aile_ard" in f.name],
            },

            {
                "title": "Aile arrière gauche",
                "icon": "icons/aile_ar.png",
                "fields": [f for f in form if "aile_arg" in f.name],
            },

            {
                "title": "Élargisseur d'aile avant droite",
                "icon": "icons/elargisseur.png",
                "fields": [f for f in form if "elargisseur_ail_avd" in f.name],
            },
            {
                "title": "Élargisseur d'aile avant gauche",
                "icon": "icons/elargisseur.png",
                "fields": [f for f in form if "elargisseur_ail_avg" in f.name],
            },
            {
                "title": "Élargisseur d'aile arrière droite",
                "icon": "icons/elargisseur.png",
                "fields": [f for f in form if "elargisseur_ail_ard" in f.name],
            },
            {
                "title": "Élargisseur d'aile arrière gauche",
                "icon": "icons/elargisseur.png",
                "fields": [f for f in form if "elargisseur_ail_arg" in f.name],
            },

            {
                "title": "Bas de caisse droit",
                "icon": "icons/bas-de-caisse.png",
                "fields": [f for f in form if "bas_de_caisse_d" in f.name],
            },
            {
                "title": "Bas de caisse gauche",
                "icon": "icons/bas-de-caisse.png",
                "fields": [f for f in form if "bas_de_caisse_g" in f.name],
            },
            {
                "title": "Porte avant droite",
                "icon": "icons/porte-de-voiture.png",
                "fields": [f for f in form if "porte_avd_po" in f.name],
            },
            {
                "title": "Porte avant gauche",
                "icon": "icons/porte-de-voiture.png",
                "fields": [f for f in form if "porte_avg_po" in f.name],
            },
            {
                "title": "Porte arrière droite",
                "icon": "icons/porte-de-voiture.png",
                "fields": [f for f in form if "porte_ard_po" in f.name],
            },
            {
                "title": "Porte arrière gauche",
                "icon": "icons/porte-de-voiture.png",
                "fields": [f for f in form if "porte_arg_po" in f.name],
            },

            {
                "title": "Coffre",
                "icon": "icons/coffre.png",
                "fields": [f for f in form if "coffre_hai" in f.name],
            },

            {
                "title": "Capot",
                "icon": "icons/capot.png",
                "fields": [f for f in form if "capot_pi" in f.name],
            },

            {
                "title": "Joint de coffre",
                "icon": "icons/joint.png",
                "fields": [f for f in form if "joint_coffre" in f.name],
            },
            {
                "title": "Joint de porte avant droite",
                "icon": "icons/joint.png",
                "fields": [f for f in form if "joint_porte_avd" in f.name],
            },
            {
                "title": "Joint de porte avant gauche",
                "icon": "icons/joint.png",
                "fields": [f for f in form if "joint_porte_avg" in f.name],
            },
            {
                "title": "Joint de porte arrière droite",
                "icon": "icons/joint.png",
                "fields": [f for f in form if "joint_porte_ard" in f.name],
            },
            {
                "title": "Joint de porte arrière gauche",
                "icon": "icons/joint.png",
                "fields": [f for f in form if "joint_porte_arg" in f.name],
            },
            {
                "title": "Coquille d'aile avant droite",
                "icon": "icons/aile.png",
                "fields": [f for f in form if "coquille_ai_avd" in f.name],
            },
            {
                "title": "Coquille d'aile avant gauche",
                "icon": "icons/aile.png",
                "fields": [f for f in form if "coquille_ai_avg" in f.name],
            },
            {
                "title": "Coquille d'aile arrière droite",
                "icon": "icons/aile.png",
                "fields": [f for f in form if "coquille_ai_ard" in f.name],
            },
            {
                "title": "Coquille d'aile arrière gauche",
                "icon": "icons/aile.png",
                "fields": [f for f in form if "coquille_ai_arg" in f.name],
            },

            {
                "title": "Support de radiateur",
                "icon": "icons/radiateur.png",
                "fields": [f for f in form if "support_radiateur" in f.name],
            },

            # Pare-brise
            {
                "title": "Pare-brise",
                "icon": "icons/pare-brise-casse.png",
                "fields": [f for f in form if "pa_brise" in f.name],
            },

            # Vitres de portes
            {
                "title": "Vitre de porte avant droite",
                "icon": "icons/vitre.png",
                "fields": [f for f in form if "vitre_porte_avd" in f.name],
            },
            {
                "title": "Vitre de porte avant gauche",
                "icon": "icons/vitre.png",
                "fields": [f for f in form if "vitre_porte_avg" in f.name],
            },
            {
                "title": "Vitre de porte arrière droite",
                "icon": "icons/vitre.png",
                "fields": [f for f in form if "vitre_porte_ard" in f.name],
            },
            {
                "title": "Vitre de porte arrière gauche",
                "icon": "icons/vitre.png",
                "fields": [f for f in form if "vitre_porte_arg" in f.name],
            },

            # Lunette arrière
            {
                "title": "Lunette / vitre arrière",
                "icon": "icons/lunette.png",
                "fields": [f for f in form if "lunette" in f.name],
            },

            # Rétroviseurs
            {
                "title": "Rétroviseur droit",
                "icon": "icons/retro.png",
                "fields": [f for f in form if "retroviseur_d" in f.name],
            },
            {
                "title": "Rétroviseur gauche",
                "icon": "icons/retro.png",
                "fields": [f for f in form if "retroviseur_g" in f.name],
            },

            # Phares
            {
                "title": "Phare avant droit",
                "icon": "icons/phares.png",
                "fields": [f for f in form if "phare_avd" in f.name],
            },
            {
                "title": "Phare avant gauche",
                "icon": "icons/phares.png",
                "fields": [f for f in form if "phare_avg" in f.name],
            },
            {
                "title": "Feu arrière droit",
                "icon": "icons/phares.png",
                "fields": [f for f in form if "phare_ard" in f.name],
            },
            {
                "title": "Feu arrière gauche",
                "icon": "icons/phares.png",
                "fields": [f for f in form if "phare_arg" in f.name],
            },
            # Anti-brouillards
            {
                "title": "Anti-brouillard avant droit",
                "icon": "icons/phares.png",
                "fields": [f for f in form if "anti_brouillard_avd" in f.name],
            },
            {
                "title": "Anti-brouillard avant gauche",
                "icon": "icons/phares.png",
                "fields": [f for f in form if "anti_brouillard_avg" in f.name],
            },
            {
                "title": "Anti-brouillard arrière",
                "icon": "icons/phares.png",
                "fields": [f for f in form if "anti_brouillard_ar" in f.name],
            },

            {
                "title": "Clignotant avant droit",
                "icon": "icons/clignotant.png",
                "fields": [f for f in form if "clignotant_avd" in f.name],
            },
            {
                "title": "Clignotant avant gauche",
                "icon": "icons/clignotant.png",
                "fields": [f for f in form if "clignotant_avg" in f.name],
            },
            {
                "title": "Clignotant arrière droit",
                "icon": "icons/clignotant.png",
                "fields": [f for f in form if "clignotant_ard" in f.name],
            },
            {
                "title": "Clignotant arrière gauche",
                "icon": "icons/clignotant.png",
                "fields": [f for f in form if "clignotant_arg" in f.name],
            },

            # Troisième feu stop
            {
                "title": "Troisième feu stop",
                "icon": "icons/feu-stop.png",
                "fields": [f for f in form if "troisieme_feu_stop" in f.name],
            },

            # Capteur de recul
            {
                "title": "Capteur de recul",
                "icon": "icons/capteurs.png",
                "fields": [f for f in form if "capteur_recul" in f.name],
            },


            # Clips et visserie
            {
                "title": "Clips",
                "icon": "icons/clips.png",
                "fields": [f for f in form if "clips" in f.name],
            },

            {
                "title": "Visserie",
                "icon": "icons/visserie.png",
                "fields": [f for f in form if "visserie" in f.name],
            },

            {
                "title": "Peinture aile avant droite",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_avant_droit" in f.name],
            },
            {
                "title": "Peinture aile avant gauche",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_avant_gauche" in f.name],
            },
            # Aile arrière droite
            {
                "title": "Peinture aile arrière droite",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_arriere_droit" in f.name],
            },

            # Aile arrière gauche
            {
                "title": "Peinture aile arrière gauche",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_arriere_gauche" in f.name],
            },

            # Face avant
            {
                "title": "Peinture face avant",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_face_avant" in f.name],
            },

            # Capot
            {
                "title": "Peinture capot",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_capot" in f.name],
            },

            # Arrière complet
            {
                "title": "Peinture arrière complete",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_arriere_complete" in f.name],
            },

            # Peinture complète
            {
                "title": "Peinture complète",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_complete" in f.name],
            },



            {
                "title": "Etiquette",
                "icon": "icons/tag.png",
                "fields": [f for f in form if "tag" in f.name],
            },
            {
                "title": "Remarques",
                "icon": "icons/notes.png",
                "fields": [f for f in form if "remarques" in f.name],
            },
            {
                "title": "Technicien",
                "icon": "icons/mecanicien.png",
                "fields": [f for f in form if "tech" in f.name],
            },
        ]

        return render(request, 'carrosserie_interne/carrosserie_interne_create.html', {
            "exemplaire": exemplaire,
            "maintenance": maintenance,
            "form": form,
            "sections": sections,  # 🔥 IMPORTANT
            "now": timezone.now(),
        })




# ------------
# Vue détail carrosserie_interne
# -----------------------------
@login_required
def carrosserie_interne_detail_view(request, carrosserie_interne_id):
    carrosserie_interne = get_object_or_404(
       CarrosserieInterne.objects.select_related("voiture_exemplaire"),
        id=carrosserie_interne_id
    )

    context = {
        "carrosserie_interne": carrosserie_interne,
        "exemplaire": carrosserie_interne.voiture_exemplaire,
    }
    return render(request, "carrosserie_interne/carrosserie_interne_detail.html", context)






@login_required
def modifier_carrosserie_interne_view(request, carrosserie_interne_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération de l'objet CarrosserieInterne avec son exemplaire
        carrosserie_interne = get_object_or_404(
            CarrosserieInterne.objects.select_related("voiture_exemplaire"),
            id=carrosserie_interne_id
        )

        exemplaire = carrosserie_interne.voiture_exemplaire

        # -------------------------
        # Gestion POST
        # -------------------------
        if request.method == "POST":
            form = CarrosserieInterneForm(
                request.POST,
                instance=carrosserie_interne,
                user=request.user,
                exemplaire=carrosserie_interne.voiture_exemplaire
            )
            if form.is_valid():
                form.save()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=_("Modification carrosserie - %(immatriculation)s") % {
                        "immatriculation": exemplaire.immatriculation
                    }
                )

                messages.success(request, _("Carrosserie modifiée avec succès !"))
   
            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
                print(form.errors)

        # -------------------------
        # Gestion GET
        # -------------------------
        else:
            form = CarrosserieInterneForm(
                instance=carrosserie_interne,
                user=request.user,
                exemplaire=carrosserie_interne.voiture_exemplaire
            )

        # -------------------------
        # Organisation des champs par sections pour le template
        # -------------------------
        sections = [
            {
                "title": "Kilométrage",
                "icon": "icons/compteur.png",
                "fields": [f for f in form if "kilo" in f.name],
            },
            {
                "title": "Pare-chocs avant",
                "icon": "icons/pare-chocs.png",
                "fields": [f for f in form if "pare_choc_av" in f.name],
            },
            {
                "title": "Pare-chocs arrière",
                "icon": "icons/pare-chocs.png",
                "fields": [f for f in form if "pare_choc_ar" in f.name],
            },
            {
                "title": "Traverse avant",
                "icon": "icons/pare-chocs.png",
                "fields": [f for f in form if "bouclier_av" in f.name],
            },
            {
                "title": "Traverse arrière",
                "icon": "icons/pare-chocs.png",
                "fields": [f for f in form if "bouclier_ar" in f.name],
            },

            {
                "title": "Support pare-chocs avant",
                "icon": "icons/pare-chocs.png",
                "fields": [f for f in form if "support_pa_choc_av" in f.name],
            },
            {
                "title": "Support pare-chocs arrière",
                "icon": "icons/pare-chocs.png",
                "fields": [f for f in form if "support_pa_choc_ar" in f.name],
            },

            {
                "title": "Calandre",
                "icon": "icons/calandre.png",
                "fields": [f for f in form if "calandre" in f.name],
            },
            {
                "title": "Aile avant droite",
                "icon": "icons/aile.png",
                "fields": [f for f in form if "aile_avd" in f.name],
            },

            {
                "title": "Aile avant gauche",
                "icon": "icons/aile.png",
                "fields": [f for f in form if "aile_avg" in f.name],
            },
            {
                "title": "Aile arrière droite",
                "icon": "icons/aile_ar.png",
                "fields": [f for f in form if "aile_ard" in f.name],
            },

            {
                "title": "Aile arrière gauche",
                "icon": "icons/aile_ar.png",
                "fields": [f for f in form if "aile_arg" in f.name],
            },

            {
                "title": "Élargisseur d'aile avant droite",
                "icon": "icons/elargisseur.png",
                "fields": [f for f in form if "elargisseur_ail_avd" in f.name],
            },
            {
                "title": "Élargisseur d'aile avant gauche",
                "icon": "icons/elargisseur.png",
                "fields": [f for f in form if "elargisseur_ail_avg" in f.name],
            },
            {
                "title": "Élargisseur d'aile arrière droite",
                "icon": "icons/elargisseur.png",
                "fields": [f for f in form if "elargisseur_ail_ard" in f.name],
            },
            {
                "title": "Élargisseur d'aile arrière gauche",
                "icon": "icons/elargisseur.png",
                "fields": [f for f in form if "elargisseur_ail_arg" in f.name],
            },

            {
                "title": "Bas de caisse droit",
                "icon": "icons/bas-de-caisse.png",
                "fields": [f for f in form if "bas_de_caisse_d" in f.name],
            },
            {
                "title": "Bas de caisse gauche",
                "icon": "icons/bas-de-caisse.png",
                "fields": [f for f in form if "bas_de_caisse_g" in f.name],
            },
            {
                "title": "Porte avant droite",
                "icon": "icons/porte-de-voiture.png",
                "fields": [f for f in form if "porte_avd_po" in f.name],
            },
            {
                "title": "Porte avant gauche",
                "icon": "icons/porte-de-voiture.png",
                "fields": [f for f in form if "porte_avg_po" in f.name],
            },
            {
                "title": "Porte arrière droite",
                "icon": "icons/porte-de-voiture.png",
                "fields": [f for f in form if "porte_ard_po" in f.name],
            },
            {
                "title": "Porte arrière gauche",
                "icon": "icons/porte-de-voiture.png",
                "fields": [f for f in form if "porte_arg_po" in f.name],
            },

            {
                "title": "Coffre",
                "icon": "icons/coffre.png",
                "fields": [f for f in form if "coffre_hai" in f.name],
            },

            {
                "title": "Capot",
                "icon": "icons/capot.png",
                "fields": [f for f in form if "capot_pi" in f.name],
            },

            {
                "title": "Joint de coffre",
                "icon": "icons/joint.png",
                "fields": [f for f in form if "joint_coffre" in f.name],
            },
            {
                "title": "Joint de porte avant droite",
                "icon": "icons/joint.png",
                "fields": [f for f in form if "joint_porte_avd" in f.name],
            },
            {
                "title": "Joint de porte avant gauche",
                "icon": "icons/joint.png",
                "fields": [f for f in form if "joint_porte_avg" in f.name],
            },
            {
                "title": "Joint de porte arrière droite",
                "icon": "icons/joint.png",
                "fields": [f for f in form if "joint_porte_ard" in f.name],
            },
            {
                "title": "Joint de porte arrière gauche",
                "icon": "icons/joint.png",
                "fields": [f for f in form if "joint_porte_arg" in f.name],
            },
            {
                "title": "Coquille d'aile avant droite",
                "icon": "icons/aile.png",
                "fields": [f for f in form if "coquille_ai_avd" in f.name],
            },
            {
                "title": "Coquille d'aile avant gauche",
                "icon": "icons/aile.png",
                "fields": [f for f in form if "coquille_ai_avg" in f.name],
            },
            {
                "title": "Coquille d'aile arrière droite",
                "icon": "icons/aile.png",
                "fields": [f for f in form if "coquille_ai_ard" in f.name],
            },
            {
                "title": "Coquille d'aile arrière gauche",
                "icon": "icons/aile.png",
                "fields": [f for f in form if "coquille_ai_arg" in f.name],
            },

            {
                "title": "Support de radiateur",
                "icon": "icons/radiateur.png",
                "fields": [f for f in form if "support_radiateur" in f.name],
            },

            # Pare-brise
            {
                "title": "Pare-brise",
                "icon": "icons/pare-brise-casse.png",
                "fields": [f for f in form if "pa_brise" in f.name],
            },

            # Vitres de portes
            {
                "title": "Vitre de porte avant droite",
                "icon": "icons/vitre.png",
                "fields": [f for f in form if "vitre_porte_avd" in f.name],
            },
            {
                "title": "Vitre de porte avant gauche",
                "icon": "icons/vitre.png",
                "fields": [f for f in form if "vitre_porte_avg" in f.name],
            },
            {
                "title": "Vitre de porte arrière droite",
                "icon": "icons/vitre.png",
                "fields": [f for f in form if "vitre_porte_ard" in f.name],
            },
            {
                "title": "Vitre de porte arrière gauche",
                "icon": "icons/vitre.png",
                "fields": [f for f in form if "vitre_porte_arg" in f.name],
            },

            # Lunette arrière
            {
                "title": "Lunette / vitre arrière",
                "icon": "icons/lunette.png",
                "fields": [f for f in form if "lunette" in f.name],
            },

            # Rétroviseurs
            {
                "title": "Rétroviseur droit",
                "icon": "icons/retro.png",
                "fields": [f for f in form if "retroviseur_d" in f.name],
            },
            {
                "title": "Rétroviseur gauche",
                "icon": "icons/retro.png",
                "fields": [f for f in form if "retroviseur_g" in f.name],
            },

            # Phares
            {
                "title": "Phare avant droit",
                "icon": "icons/phares.png",
                "fields": [f for f in form if "phare_avd" in f.name],
            },
            {
                "title": "Phare avant gauche",
                "icon": "icons/phares.png",
                "fields": [f for f in form if "phare_avg" in f.name],
            },
            {
                "title": "Feu arrière droit",
                "icon": "icons/phares.png",
                "fields": [f for f in form if "phare_ard" in f.name],
            },
            {
                "title": "Feu arrière gauche",
                "icon": "icons/phares.png",
                "fields": [f for f in form if "phare_arg" in f.name],
            },
            # Anti-brouillards
            {
                "title": "Anti-brouillard avant droit",
                "icon": "icons/phares.png",
                "fields": [f for f in form if "anti_brouillard_avd" in f.name],
            },
            {
                "title": "Anti-brouillard avant gauche",
                "icon": "icons/phares.png",
                "fields": [f for f in form if "anti_brouillard_avg" in f.name],
            },
            {
                "title": "Anti-brouillard arrière",
                "icon": "icons/phares.png",
                "fields": [f for f in form if "anti_brouillard_ar" in f.name],
            },

            {
                "title": "Clignotant avant droit",
                "icon": "icons/clignotant.png",
                "fields": [f for f in form if "clignotant_avd" in f.name],
            },
            {
                "title": "Clignotant avant gauche",
                "icon": "icons/clignotant.png",
                "fields": [f for f in form if "clignotant_avg" in f.name],
            },
            {
                "title": "Clignotant arrière droit",
                "icon": "icons/clignotant.png",
                "fields": [f for f in form if "clignotant_ard" in f.name],
            },
            {
                "title": "Clignotant arrière gauche",
                "icon": "icons/clignotant.png",
                "fields": [f for f in form if "clignotant_arg" in f.name],
            },

            # Troisième feu stop
            {
                "title": "Troisième feu stop",
                "icon": "icons/feu-stop.png",
                "fields": [f for f in form if "troisieme_feu_stop" in f.name],
            },

            # Capteur de recul
            {
                "title": "Capteur de recul",
                "icon": "icons/capteurs.png",
                "fields": [f for f in form if "capteur_recul" in f.name],
            },

            # Clips et visserie
            {
                "title": "Clips",
                "icon": "icons/clips.png",
                "fields": [f for f in form if "clips" in f.name],
            },

            {
                "title": "Visserie",
                "icon": "icons/visserie.png",
                "fields": [f for f in form if "visserie" in f.name],
            },

            {
                "title": "Peinture aile avant droite",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_avant_droit" in f.name],
            },
            {
                "title": "Peinture aile avant gauche",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_avant_gauche" in f.name],
            },
            # Aile arrière droite
            {
                "title": "Peinture aile arrière droite",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_arriere_droit" in f.name],
            },

            # Aile arrière gauche
            {
                "title": "Peinture aile arrière gauche",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_arriere_gauche" in f.name],
            },

            # Face avant
            {
                "title": "Peinture face avant",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_face_avant" in f.name],
            },

            # Capot
            {
                "title": "Peinture capot",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_capot" in f.name],
            },

            # Arrière complet
            {
                "title": "Peinture arrière complete",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_arriere_complete" in f.name],
            },

            # Peinture complète
            {
                "title": "Peinture complète",
                "icon": "icons/pistolet-a-peinture.png",
                "fields": [f for f in form if "peinture_complete" in f.name],
            },

            {
                "title": "Etiquette",
                "icon": "icons/tag.png",
                "fields": [f for f in form if "tag" in f.name],
            },
            {
                "title": "Remarques",
                "icon": "icons/notes.png",
                "fields": [f for f in form if "remarques" in f.name],
            },
            {
                "title": "Technicien",
                "icon": "icons/mecanicien.png",
                "fields": [f for f in form if "tech" in f.name],
            },
        ]

    return render(
        request,
        "carrosserie_interne/modifier_carrosserie_interne.html",
        {
            "form": form,
            "carrosserie_interne": carrosserie_interne,
            "exemplaire": carrosserie_interne.voiture_exemplaire,
            "sections": sections,
        }
    )



@login_required
def rapport_view(request, pk):
    obj = get_object_or_404(CarrosserieInterne, pk=pk)

    rapport = obj.generer_rapport_remplacement()

    return render(request, "carrosserie_interne/rapport.html", {
        "rapport": rapport,
        "obj": obj
    })




@login_required
def carrosserie_interne_pdf_view(request, carrosserie_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        carrosserie = get_object_or_404(
            CarrosserieInterne.objects.select_related(
                "voiture_exemplaire",
                "tech_technicien",
                "tech_societe",
                "main_oeuvre",
            ),
            id=carrosserie_id
        )

        html_string = render_to_string(
            "carrosserie_interne/carrosserie_interne_pdf.html",
            {
                "carrosserie": carrosserie,
                "societe": tenant,
            }
        )

        pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="carrosserie_interne_{carrosserie.id}.pdf"'
        )
        return response