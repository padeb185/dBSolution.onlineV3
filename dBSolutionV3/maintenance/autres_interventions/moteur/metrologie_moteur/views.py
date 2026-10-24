from datetime import datetime
from decimal import Decimal

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _, gettext_noop
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from weasyprint import HTML

from maintenance.models import Maintenance
from utilisateurs.models import UserLog
from utils.securite import q_intervention_tenant
from voiture.voiture_exemplaire.models import VoitureExemplaire

from ..moteur_lie import moteur_actuel
from .forms import MesureCylindreFormSet, MesureTourillonFormSet, MetrologieMoteurForm
from .models import MetrologieMoteur

ROLES_AUTORISES = ["mecanicien", "apprenti", "magasinier", "chef_mecanicien", "direction"]
ROLES_SUPPRESSION = ["direction", "chef_mecanicien"]


def _exemplaires_tenant(user):
    tenant = user.societe
    return VoitureExemplaire.objects.filter(Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant))


def _sections(form):
    """Sections du formulaire principal (les mesures par cylindre / tourillon sont des tableaux à part)."""
    def champs(*noms):
        return [form[n] for n in noms if n in form.fields]

    def prefixe(p):
        return [form[f.name] for f in form if f.name.startswith(p)]

    return {
        "kilometrage": champs("kilometres_chassis", "kilometrage_metrologie", "kilometrage_variation"),
        "moteur": champs("nombre_cylindres", "alesage_nominal", "course_nominale", "cylindree_constructeur_cm3"),
        "cylindree": champs("alesage_mesure", "course_mesuree", "cylindree_cm3"),
        "tol_chemise": prefixe("tol_chemise_") + prefixe("tol_jeu_piston_"),
        "tol_segments": prefixe("tol_segment_"),
        "tol_vilebrequin": prefixe("tol_maneton_") + prefixe("tol_tourillon_"),
        "tol_bielle": prefixe("tol_pied_bielle_") + prefixe("tol_jeu_pied_bielle_"),
        "divers": champs("tag", "pays", "remarques"),
        "technicien": champs("tech_technicien", "tech_nom_technicien", "tech_role_technicien", "tech_societe"),
        "main_oeuvre": champs("taux_horaire"),
    }


def _contexte(form, cylindres_fs, tourillons_fs, exemplaire, metrologie=None):
    return {
        "form": form,
        "sections": _sections(form),
        "cylindres_fs": cylindres_fs,
        "tourillons_fs": tourillons_fs,
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation if exemplaire else "",
        "metrologie": metrologie,
        "now": timezone.now(),
    }


def _formset_initial(formset_class, nombre, prefix):
    factory = forms.inlineformset_factory(
        MetrologieMoteur, formset_class.model, form=formset_class.form, extra=nombre, can_delete=True,
    )
    return factory(instance=MetrologieMoteur(), prefix=prefix,
                   initial=[{"numero": i} for i in range(1, nombre + 1)])


def _enregistrer_lignes(obj, cylindres_fs, tourillons_fs):
    cylindres_fs.instance = obj
    cylindres_fs.save()
    tourillons_fs.instance = obj
    tourillons_fs.save()
    obj.finaliser()


# ------------------------------------------------------------------
# LISTE
# ------------------------------------------------------------------
@method_decorator([login_required, never_cache], name="dispatch")
class MetrologieMoteurListView(ListView):
    model = MetrologieMoteur
    template_name = "metrologie_moteur/metrologie_list.html"
    context_object_name = "metrologies"

    def get_queryset(self):
        qs = MetrologieMoteur.objects.select_related(
            "voiture_exemplaire", "maintenance", "tech_societe", "main_oeuvre"
        ).filter(q_intervention_tenant(self.request.user))
        exemplaire_id = self.kwargs.get("exemplaire_id")
        if exemplaire_id:
            qs = qs.filter(voiture_exemplaire_id=exemplaire_id)
        return qs.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["exemplaire"] = get_object_or_404(_exemplaires_tenant(self.request.user), id=self.kwargs.get("exemplaire_id"))
        context["is_checkup_allowed"] = self.request.user.role in ROLES_AUTORISES
        return context


# ------------------------------------------------------------------
# CRÉATION
# ------------------------------------------------------------------
@never_cache
@login_required
def metrologie_form_view(request, exemplaire_id):
    role = request.user.role
    exemplaire = get_object_or_404(_exemplaires_tenant(request.user), id=exemplaire_id)

    if role not in ROLES_AUTORISES:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    if request.method == "POST":
        form = MetrologieMoteurForm(request.POST, user=request.user, exemplaire=exemplaire)
        cylindres_fs = MesureCylindreFormSet(request.POST, instance=MetrologieMoteur(), prefix="cyl")
        tourillons_fs = MesureTourillonFormSet(request.POST, instance=MetrologieMoteur(), prefix="tour")

        if form.is_valid() and cylindres_fs.is_valid() and tourillons_fs.is_valid():
            try:
                ancien_km = exemplaire.kilometres_chassis or 0
                ancien_km_boite = exemplaire.kilometres_boite or 0
                ancien_km_moteur = exemplaire.kilometres_moteur or 0
                ancien_km_embrayage = exemplaire.kilometres_embrayage or 0
                km = int(form.cleaned_data["kilometrage_metrologie"])

                with transaction.atomic():
                    # Rollback véhicule
                    exemplaire.kilometres_rollback = ancien_km
                    exemplaire.kilometres_boite_rollback = ancien_km_boite
                    exemplaire.kilometres_moteur_rollback = ancien_km_moteur
                    exemplaire.kilometres_embrayage_rollback = ancien_km_embrayage
                    exemplaire.date_derniere_intervention = timezone.localtime(timezone.now()).date()
                    exemplaire.kilometres_chassis = km
                    exemplaire.update_kilometres()
                    exemplaire.save(update_fields=[
                        "kilometres_chassis", "date_derniere_intervention",
                        "kilometres_rollback", "kilometres_boite_rollback",
                        "kilometres_moteur_rollback", "kilometres_embrayage_rollback",
                        "kilometres_moteur", "kilometres_boite", "kilometres_embrayage", "variation_kilometres",
                    ])

                    maintenance = Maintenance.objects.create(
                        societe=request.user.societe,
                        voiture_exemplaire=exemplaire,
                        immatriculation=exemplaire.immatriculation,
                        date_intervention=timezone.now().date(),
                        kilometres_chassis=exemplaire.kilometres_chassis,
                        kilometres_dernier_entretien=exemplaire.kilometres_dernier_entretien,
                        type_maintenance=Maintenance.TypeMaintenance.METROLOGIE_MOTEUR,
                        tag=Maintenance.Tag.JAUNE,
                    )
                    if role == "mecanicien":
                        maintenance.mecanicien = request.user
                    elif role == "chef_mecanicien":
                        maintenance.chef_mecanicien = request.user
                    elif role == "apprenti":
                        maintenance.apprentis.add(request.user)
                    elif role == "magasinier":
                        maintenance.magasinier = request.user
                    elif role == "direction":
                        maintenance.direction = request.user
                    maintenance.save()

                    obj = form.save(commit=False)
                    obj.voiture_exemplaire = exemplaire
                    obj.maintenance = maintenance
                    obj.kilometres_chassis = ancien_km
                    obj.kilometres_boite = ancien_km_boite
                    obj.kilometres_moteur = ancien_km_moteur
                    obj.kilometres_embrayage = ancien_km_embrayage
                    obj.kilometrage_metrologie = km
                    obj.assign_technicien(request.user)
                    form.enregistrer_main_oeuvre(obj)
                    obj.save()
                    _enregistrer_lignes(obj, cylindres_fs, tourillons_fs)

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{gettext_noop('Intervention métrologie moteur')} - {exemplaire.immatriculation}",
                )
                messages.success(request, _("Intervention enregistrée avec succès."))
                return redirect(f"{reverse('metrologie_moteur:metrologie_detail', kwargs={'metrologie_id': obj.id})}")

            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        moteur = moteur_actuel(exemplaire)
        nouveau = MetrologieMoteur(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis or 0,
            kilometres_moteur=exemplaire.kilometres_moteur or 0,
            kilometres_boite=exemplaire.kilometres_boite or 0,
            kilometres_embrayage=exemplaire.kilometres_embrayage or 0,
        )
        if moteur:
            if moteur.nombre_cylindres:
                nouveau.nombre_cylindres = moteur.nombre_cylindres
            if moteur.cylindree_l:
                nouveau.cylindree_constructeur_cm3 = (Decimal(str(moteur.cylindree_l)) * 1000).quantize(Decimal("0.1"))
        # Reprise des cotes constructeur et tolérances de la dernière métrologie de ce véhicule
        precedente = MetrologieMoteur.objects.filter(voiture_exemplaire=exemplaire).order_by("-id").first()
        if precedente:
            for f in MetrologieMoteur._meta.fields:
                if f.name.startswith("tol_") or f.name in ("nombre_cylindres", "alesage_nominal", "course_nominale",
                                                            "cylindree_constructeur_cm3"):
                    setattr(nouveau, f.name, getattr(precedente, f.name))
        nouveau.assign_technicien(request.user)

        form = MetrologieMoteurForm(instance=nouveau, user=request.user, exemplaire=exemplaire)
        # Une ligne par cylindre et une par tourillon (moteur en ligne : n + 1 paliers)
        n = nouveau.nombre_cylindres or 4
        cylindres_fs = _formset_initial(MesureCylindreFormSet, n, "cyl")
        tourillons_fs = _formset_initial(MesureTourillonFormSet, n + 1, "tour")

    return render(request, "metrologie_moteur/metrologie_form.html",
                  _contexte(form, cylindres_fs, tourillons_fs, exemplaire))


# ------------------------------------------------------------------
# DÉTAIL
# ------------------------------------------------------------------
@never_cache
@login_required
def metrologie_detail_view(request, metrologie_id):
    metrologie = get_object_or_404(
        MetrologieMoteur.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=metrologie_id,
    )
    return render(request, "metrologie_moteur/metrologie_detail.html", {
        "metrologie": metrologie,
        "exemplaire": metrologie.voiture_exemplaire,
    })


# ------------------------------------------------------------------
# MODIFICATION
# ------------------------------------------------------------------
@never_cache
@login_required
def modifier_metrologie_view(request, metrologie_id):
    metrologie = get_object_or_404(
        MetrologieMoteur.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=metrologie_id,
    )
    exemplaire = metrologie.voiture_exemplaire

    if request.user.role not in ROLES_AUTORISES and not request.user.is_superuser:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    if request.method == "POST":
        km_avant = metrologie.kilometres_chassis or 0
        form = MetrologieMoteurForm(request.POST, instance=metrologie, user=request.user, exemplaire=exemplaire)
        cylindres_fs = MesureCylindreFormSet(request.POST, instance=metrologie, prefix="cyl")
        tourillons_fs = MesureTourillonFormSet(request.POST, instance=metrologie, prefix="tour")

        if form.is_valid() and cylindres_fs.is_valid() and tourillons_fs.is_valid():
            try:
                with transaction.atomic():
                    km = form.cleaned_data.get("kilometrage_metrologie")
                    km = int(km) if km is not None else None

                    if km is not None and km < 0:
                        raise ValidationError(_("Le kilométrage ne peut pas être négatif."))

                    obj = form.save(commit=False)
                    obj.voiture_exemplaire = exemplaire
                    obj.kilometrage_metrologie = km
                    obj.assign_technicien(request.user)
                    form.enregistrer_main_oeuvre(obj)

                    if exemplaire and km is not None:
                        exemplaire.date_derniere_intervention = timezone.localtime(timezone.now()).date()
                        if km >= (exemplaire.kilometres_chassis or 0):
                            exemplaire.kilometres_chassis = km
                        exemplaire.save()

                    obj.kilometres_chassis = km_avant
                    obj.save()
                    _enregistrer_lignes(obj, cylindres_fs, tourillons_fs)

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{gettext_noop('Modification intervention métrologie moteur')} - {exemplaire.immatriculation if exemplaire else ''}",
                )
                messages.success(request, _("Intervention modifiée avec succès !"))
                return redirect(reverse("metrologie_moteur:metrologie_detail", kwargs={"metrologie_id": metrologie.id}))

            except ValidationError as e:
                form.add_error(None, e)
                messages.error(request, _("Kilométrage invalide"))
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form = MetrologieMoteurForm(instance=metrologie, user=request.user, exemplaire=exemplaire)
        cylindres_fs = MesureCylindreFormSet(instance=metrologie, prefix="cyl")
        tourillons_fs = MesureTourillonFormSet(instance=metrologie, prefix="tour")

    return render(request, "metrologie_moteur/metrologie_form.html",
                  _contexte(form, cylindres_fs, tourillons_fs, exemplaire, metrologie))


# ------------------------------------------------------------------
# SUPPRESSION
# ------------------------------------------------------------------
@never_cache
@login_required
def delete_metrologie_view(request, metrologie_id):
    if request.user.role not in ROLES_SUPPRESSION and not request.user.is_superuser:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    metrologie = get_object_or_404(
        MetrologieMoteur.objects.select_related("voiture_exemplaire", "maintenance").filter(
            q_intervention_tenant(request.user)),
        id=metrologie_id,
    )
    exemplaire = metrologie.voiture_exemplaire
    maintenance = metrologie.maintenance

    if request.method == "POST":
        try:
            with transaction.atomic():
                immatriculation = exemplaire.immatriculation if exemplaire else ""
                if exemplaire:
                    exemplaire.kilometres_chassis = exemplaire.kilometres_rollback or 0
                    exemplaire.kilometres_boite = exemplaire.kilometres_boite_rollback or 0
                    exemplaire.kilometres_moteur = exemplaire.kilometres_moteur_rollback or 0
                    exemplaire.kilometres_embrayage = exemplaire.kilometres_embrayage_rollback or 0
                    exemplaire.save(update_fields=[
                        "kilometres_chassis", "kilometres_boite", "kilometres_moteur", "kilometres_embrayage",
                    ])
                metrologie.delete()
                if maintenance:
                    maintenance.delete()
                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{gettext_noop('Suppression de l’intervention métrologie moteur')} - {immatriculation}",
                )
            messages.success(request, _("Intervention supprimée avec succès."))
            if exemplaire:
                return redirect(reverse("metrologie_moteur:metrologie_list", kwargs={"exemplaire_id": exemplaire.id}))
            return redirect("utilisateurs:dashboard")
        except Exception as e:
            messages.error(request, _("Erreur lors de la suppression : %(erreur)s") % {"erreur": str(e)})

    return render(request, "metrologie_moteur/delete_metrologie.html", {
        "metrologie": metrologie,
        "exemplaire": exemplaire,
    })


# ------------------------------------------------------------------
# PDF
# ------------------------------------------------------------------
@login_required
def metrologie_detail_pdf_view(request, pk):
    metrologie = get_object_or_404(
        MetrologieMoteur.objects.select_related("voiture_exemplaire", "tech_societe").filter(
            q_intervention_tenant(request.user)),
        pk=pk,
    )
    html_string = render_to_string("metrologie_moteur/metrologie_detail_pdf.html", {
        "metrologie": metrologie,
        "rapport": metrologie.generer_rapport_remplacement(),
        "date_export": datetime.now(),
        "societe": request.user.societe,
    }, request=request)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    immatriculation = metrologie.voiture_exemplaire.immatriculation if metrologie.voiture_exemplaire else "sans_immatriculation"
    technicien = str(metrologie.tech_nom_technicien or "technicien_inconnu").replace(" ", "_")
    date_pdf = (metrologie.date or timezone.now()).strftime("%Y-%m-%d")
    titre = str(_("Métrologie moteur")).replace(" ", "_").replace("'", "")
    nom_fichier = f"{titre}_{technicien}_{str(immatriculation).replace(' ', '_')}_{date_pdf}.pdf"

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{nom_fichier}"'
    return response
