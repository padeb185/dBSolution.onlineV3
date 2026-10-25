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
from .forms import CasseMoteurForm, EssaiCylindreFormSet, PieceCasseeFormSet
from .models import PISTES_DIAGNOSTIC, CasseMoteur

ROLES_AUTORISES = ["mecanicien", "apprenti", "apprentis", "magasinier", "chef_mecanicien", "direction"]
ROLES_SUPPRESSION = ["direction", "chef_mecanicien"]


def _exemplaires_tenant(user):
    tenant = user.societe
    return VoitureExemplaire.objects.filter(Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant))


def _sections(form):
    def champs(*noms):
        return [form[n] for n in noms if n in form.fields]

    return {
        "kilometrage": champs("kilometres_chassis", "kilometrage_casse", "kilometrage_variation"),
        "circonstances": champs("date_casse", "sur_piste", "circonstances"),
        "symptomes": champs(*CasseMoteur.CHAMPS_SYMPTOMES),
        "essais": champs("nombre_cylindres", "compression_nominale_bar", "ecart_compression_max_pct", "fuite_max_pct"),
        "constats": champs("analyse_huile", "endoscopie"),
        "conclusion": champs("cause_probable", "cause_precision", "decision", "prise_en_garantie"),
        "divers": champs("tag", "pays", "remarques"),
        "technicien": champs("tech_technicien", "tech_nom_technicien", "tech_role_technicien", "tech_societe"),
        "main_oeuvre": champs("taux_horaire"),
    }


def _contexte(form, pieces_fs, essais_fs, exemplaire, casse=None):
    return {
        "form": form,
        "sections": _sections(form),
        "pieces_fs": pieces_fs,
        "essais_fs": essais_fs,
        "exemplaire": exemplaire,
        "immatriculation": exemplaire.immatriculation if exemplaire else "",
        "casse": casse,
        "now": timezone.now(),
        "pistes": [[list(c), str(m)] for c, m in PISTES_DIAGNOSTIC],
    }


def _formset_initial(formset_class, nombre, prefix):
    factory = forms.inlineformset_factory(
        CasseMoteur, formset_class.model, form=formset_class.form, extra=nombre, can_delete=True,
    )
    return factory(instance=CasseMoteur(), prefix=prefix,
                   initial=[{"numero": i} for i in range(1, nombre + 1)])


def _enregistrer_lignes(obj, pieces_fs, essais_fs):
    pieces_fs.instance = obj
    pieces_fs.save()
    essais_fs.instance = obj
    essais_fs.save()


# ------------------------------------------------------------------
# LISTE
# ------------------------------------------------------------------
@method_decorator([login_required, never_cache], name="dispatch")
class CasseMoteurListView(ListView):
    model = CasseMoteur
    template_name = "casse_moteur/casse_list.html"
    context_object_name = "casses"

    def get_queryset(self):
        qs = CasseMoteur.objects.select_related(
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
def casse_form_view(request, exemplaire_id):
    role = request.user.role
    exemplaire = get_object_or_404(_exemplaires_tenant(request.user), id=exemplaire_id)

    if role not in ROLES_AUTORISES:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    if request.method == "POST":
        form = CasseMoteurForm(request.POST, user=request.user, exemplaire=exemplaire)
        pieces_fs = PieceCasseeFormSet(request.POST, instance=CasseMoteur(), prefix="piece")
        essais_fs = EssaiCylindreFormSet(request.POST, instance=CasseMoteur(), prefix="essai")

        if form.is_valid() and pieces_fs.is_valid() and essais_fs.is_valid():
            try:
                ancien_km = exemplaire.kilometres_chassis or 0
                ancien_km_boite = exemplaire.kilometres_boite or 0
                ancien_km_moteur = exemplaire.kilometres_moteur or 0
                ancien_km_embrayage = exemplaire.kilometres_embrayage or 0
                km = int(form.cleaned_data["kilometrage_casse"])

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
                        type_maintenance=Maintenance.TypeMaintenance.CASSE_MOTEUR,
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
                    obj.kilometrage_casse = km
                    obj.assign_technicien(request.user)
                    form.enregistrer_main_oeuvre(obj)
                    obj.save()
                    _enregistrer_lignes(obj, pieces_fs, essais_fs)

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{gettext_noop('Intervention casse moteur')} - {exemplaire.immatriculation}",
                )
                messages.success(request, _("Intervention enregistrée avec succès."))
                return redirect(f"{reverse('casse_moteur:casse_detail', kwargs={'casse_id': obj.id})}")

            except Exception as e:
                messages.error(request, _("Erreur lors de l'enregistrement : %(erreur)s") % {"erreur": str(e)})
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        moteur = moteur_actuel(exemplaire)
        nouveau = CasseMoteur(
            voiture_exemplaire=exemplaire,
            kilometres_chassis=exemplaire.kilometres_chassis or 0,
            kilometres_moteur=exemplaire.kilometres_moteur or 0,
            kilometres_boite=exemplaire.kilometres_boite or 0,
            kilometres_embrayage=exemplaire.kilometres_embrayage or 0,
            kilometrage_casse=exemplaire.kilometres_chassis or 0,
            date_casse=timezone.localdate(),
        )
        if moteur and moteur.nombre_cylindres:
            nouveau.nombre_cylindres = moteur.nombre_cylindres
        nouveau.assign_technicien(request.user)

        form = CasseMoteurForm(instance=nouveau, user=request.user, exemplaire=exemplaire)
        pieces_fs = PieceCasseeFormSet(instance=CasseMoteur(), prefix="piece")
        # une ligne d'essai par cylindre
        essais_fs = _formset_initial(EssaiCylindreFormSet, nouveau.nombre_cylindres or 4, "essai")

    return render(request, "casse_moteur/casse_form.html",
                  _contexte(form, pieces_fs, essais_fs, exemplaire))


# ------------------------------------------------------------------
# DÉTAIL
# ------------------------------------------------------------------
@never_cache
@login_required
def casse_detail_view(request, casse_id):
    casse = get_object_or_404(
        CasseMoteur.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=casse_id,
    )
    return render(request, "casse_moteur/casse_detail.html", {
        "casse": casse,
        "exemplaire": casse.voiture_exemplaire,
    })


# ------------------------------------------------------------------
# MODIFICATION
# ------------------------------------------------------------------
@never_cache
@login_required
def modifier_casse_view(request, casse_id):
    casse = get_object_or_404(
        CasseMoteur.objects.select_related("voiture_exemplaire").filter(q_intervention_tenant(request.user)),
        id=casse_id,
    )
    exemplaire = casse.voiture_exemplaire

    if request.user.role not in ROLES_AUTORISES and not request.user.is_superuser:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    if request.method == "POST":
        km_avant = casse.kilometres_chassis or 0
        form = CasseMoteurForm(request.POST, instance=casse, user=request.user, exemplaire=exemplaire)
        pieces_fs = PieceCasseeFormSet(request.POST, instance=casse, prefix="piece")
        essais_fs = EssaiCylindreFormSet(request.POST, instance=casse, prefix="essai")

        if form.is_valid() and pieces_fs.is_valid() and essais_fs.is_valid():
            try:
                with transaction.atomic():
                    km = form.cleaned_data.get("kilometrage_casse")
                    km = int(km) if km is not None else None

                    if km is not None and km < 0:
                        raise ValidationError(_("Le kilométrage ne peut pas être négatif."))

                    obj = form.save(commit=False)
                    obj.voiture_exemplaire = exemplaire
                    obj.kilometrage_casse = km
                    obj.assign_technicien(request.user)
                    form.enregistrer_main_oeuvre(obj)

                    if exemplaire and km is not None:
                        exemplaire.date_derniere_intervention = timezone.localtime(timezone.now()).date()
                        if km >= (exemplaire.kilometres_chassis or 0):
                            exemplaire.kilometres_chassis = km
                        exemplaire.save()

                    obj.kilometres_chassis = km_avant
                    obj.save()
                    _enregistrer_lignes(obj, pieces_fs, essais_fs)

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{gettext_noop('Modification intervention casse moteur')} - {exemplaire.immatriculation if exemplaire else ''}",
                )
                messages.success(request, _("Intervention modifiée avec succès !"))
                return redirect(reverse("casse_moteur:casse_detail", kwargs={"casse_id": casse.id}))

            except ValidationError as e:
                form.add_error(None, e)
                messages.error(request, _("Kilométrage invalide"))
        else:
            messages.error(request, _("Le formulaire contient des erreurs."))
    else:
        form = CasseMoteurForm(instance=casse, user=request.user, exemplaire=exemplaire)
        pieces_fs = PieceCasseeFormSet(instance=casse, prefix="piece")
        essais_fs = EssaiCylindreFormSet(instance=casse, prefix="essai")

    return render(request, "casse_moteur/casse_form.html",
                  _contexte(form, pieces_fs, essais_fs, exemplaire, casse))


# ------------------------------------------------------------------
# SUPPRESSION
# ------------------------------------------------------------------
@never_cache
@login_required
def delete_casse_view(request, casse_id):
    if request.user.role not in ROLES_SUPPRESSION and not request.user.is_superuser:
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    casse = get_object_or_404(
        CasseMoteur.objects.select_related("voiture_exemplaire", "maintenance").filter(
            q_intervention_tenant(request.user)),
        id=casse_id,
    )
    exemplaire = casse.voiture_exemplaire
    maintenance = casse.maintenance

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
                casse.delete()
                if maintenance:
                    maintenance.delete()
                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{gettext_noop('Suppression de l’intervention casse moteur')} - {immatriculation}",
                )
            messages.success(request, _("Intervention supprimée avec succès."))
            if exemplaire:
                return redirect(reverse("casse_moteur:casse_list", kwargs={"exemplaire_id": exemplaire.id}))
            return redirect("utilisateurs:dashboard")
        except Exception as e:
            messages.error(request, _("Erreur lors de la suppression : %(erreur)s") % {"erreur": str(e)})

    return render(request, "casse_moteur/delete_casse.html", {
        "casse": casse,
        "exemplaire": exemplaire,
    })


# ------------------------------------------------------------------
# PDF
# ------------------------------------------------------------------
@login_required
def casse_detail_pdf_view(request, pk):
    casse = get_object_or_404(
        CasseMoteur.objects.select_related("voiture_exemplaire", "tech_societe").filter(
            q_intervention_tenant(request.user)),
        pk=pk,
    )
    html_string = render_to_string("casse_moteur/casse_detail_pdf.html", {
        "casse": casse,
        "rapport": casse.generer_rapport_remplacement(),
        "date_export": datetime.now(),
        "societe": request.user.societe,
    }, request=request)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    immatriculation = casse.voiture_exemplaire.immatriculation if casse.voiture_exemplaire else "sans_immatriculation"
    technicien = str(casse.tech_nom_technicien or "technicien_inconnu").replace(" ", "_")
    date_pdf = (casse.date or timezone.now()).strftime("%Y-%m-%d")
    titre = str(_("Casse moteur")).replace(" ", "_").replace("'", "")
    nom_fichier = f"{titre}_{technicien}_{str(immatriculation).replace(' ', '_')}_{date_pdf}.pdf"

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{nom_fichier}"'
    return response
