"""
Administration des tenants (sociétés) depuis le tableau de bord admin :
liste, création (schéma + domaine + premier utilisateur), détail,
modification et création des utilisateurs d'un tenant.
Réservé aux superadministrateurs (is_staff + is_superuser).
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django_tenants.utils import get_public_schema_name, schema_context

from adresse.models import Adresse
from societe.models import Domain, Societe
from .forms_tenants import TenantCreationForm, TenantModificationForm
from .forms import UtilisateurCreationForm
from .models import UserLog, Utilisateur


def is_admin(user):
    return user.is_staff and user.is_superuser


def _log(request, action):
    try:
        UserLog.objects.create(utilisateur=request.user, action=action)
    except Exception:
        pass


def _tenants():
    return (
        Societe.objects.exclude(schema_name=get_public_schema_name())
        .select_related("adresse")
        .annotate(
            nb_utilisateurs=Count("utilisateurs", distinct=True),
            nb_actifs=Count("utilisateurs", filter=Q(utilisateurs__is_active=True), distinct=True),
        )
        .order_by("nom")
    )


# ==================================================================
# LISTE
# ==================================================================
@never_cache
@login_required
@user_passes_test(is_admin)
def tenants_liste(request):
    return render(request, "utilisateurs/tenants/tenants_liste.html", {
        "tenants": _tenants(),
    })


# ==================================================================
# CRÉATION D'UN TENANT
# ==================================================================
@never_cache
@login_required
@user_passes_test(is_admin)
def tenant_creer(request):
    form = TenantCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        try:
            # Les sociétés, domaines et utilisateurs vivent dans le schéma public.
            # La création du schéma lance les migrations du nouveau tenant (peut prendre du temps).
            with schema_context(get_public_schema_name()):
                adresse = Adresse.objects.create(
                    rue=d["rue"], numero=d["numero"], boite=d["boite"] or None,
                    code_postal=d["code_postal"], ville=d["ville"],
                    pays=d["pays"], code_pays=d["code_pays"],
                )

                societe = Societe(
                    nom=d["nom"],
                    schema_name=d["schema_name"],
                    slug=d["slug"],
                    directeur=d["directeur"],
                    numero_tva=d["numero_tva"],
                    numero_tel=d["numero_tel"] or None,
                    iban=d["iban"] or "",
                    site=d["site"] or None,
                    max_utilisateurs=d["max_utilisateurs"],
                    paid_until=d["paid_until"],
                    on_trial=d["on_trial"],
                    adresse=adresse,
                )
                societe.save()   # crée le schéma PostgreSQL + migrations

                # En mode sous-dossier (/tenant/<schema>/), le domaine = nom du schéma
                Domain.objects.create(domain=societe.schema_name, tenant=societe, is_primary=True)

                # Premier utilisateur (direction) du tenant
                if d.get("admin_email"):
                    with transaction.atomic():
                        adresse_user = Adresse.objects.create(
                            rue=d["rue"], numero=d["numero"], boite=d["boite"] or None,
                            code_postal=d["code_postal"], ville=d["ville"],
                            pays=d["pays"], code_pays=d["code_pays"],
                        )
                        Utilisateur.objects.create_user(
                            email=d["admin_email"],
                            password=d["admin_password"],
                            nom=d["admin_nom"],
                            prenom=d["admin_prenom"],
                            role="direction",
                            societe=societe,
                            schema_name=societe.schema_name,
                            adresse=adresse_user,
                        )

            _log(request, f"Création du tenant {societe.nom} ({societe.schema_name})")
            messages.success(request, _("Le tenant « %(nom)s » a été créé.") % {"nom": societe.nom})
            return redirect("utilisateurs:tenant_detail", pk=societe.pk)

        except Exception as e:
            messages.error(request, _("Erreur lors de la création du tenant : %(erreur)s") % {"erreur": e})

    return render(request, "utilisateurs/tenants/tenant_form.html", {"form": form, "societe": None})


# ==================================================================
# DÉTAIL
# ==================================================================
@never_cache
@login_required
@user_passes_test(is_admin)
def tenant_detail(request, pk):
    societe = get_object_or_404(_tenants(), pk=pk)
    utilisateurs = (
        Utilisateur.objects.filter(societe=societe)
        .order_by("-is_active", "nom", "prenom")
    )
    return render(request, "utilisateurs/tenants/tenant_detail.html", {
        "societe": societe,
        "utilisateurs": utilisateurs,
        "domaines": Domain.objects.filter(tenant=societe),
        "places_restantes": max(0, societe.max_utilisateurs - societe.nb_actifs),
    })


# ==================================================================
# MODIFICATION
# ==================================================================
@never_cache
@login_required
@user_passes_test(is_admin)
def tenant_modifier(request, pk):
    societe = get_object_or_404(_tenants(), pk=pk)
    form = TenantModificationForm(request.POST or None, instance=societe)

    if request.method == "POST" and form.is_valid():
        try:
            # Un tenant ne peut être modifié que depuis le schéma public (django-tenants)
            with schema_context(get_public_schema_name()):
                form.save()
            _log(request, f"Modification du tenant {societe.nom}")
            messages.success(request, _("Le tenant a été mis à jour."))
            return redirect("utilisateurs:tenant_detail", pk=societe.pk)
        except Exception as e:
            messages.error(request, _("Erreur lors de la mise à jour : %(erreur)s") % {"erreur": e})

    return render(request, "utilisateurs/tenants/tenant_form.html", {"form": form, "societe": societe})


# ==================================================================
# CRÉATION D'UN UTILISATEUR POUR UN TENANT
# ==================================================================
@never_cache
@login_required
@user_passes_test(is_admin)
def tenant_utilisateur_creer(request, pk):
    societe = get_object_or_404(_tenants(), pk=pk)

    initial = {"societe": societe.nom, "schema_name": societe.schema_name}
    form = UtilisateurCreationForm(request.POST or None, initial=initial)

    if request.method == "POST" and form.is_valid():
        if societe.nb_actifs >= societe.max_utilisateurs:
            messages.error(request, _(
                "Le nombre maximum d'utilisateurs de ce tenant est atteint (%(max)s). "
                "Augmentez la limite avant d'ajouter un utilisateur."
            ) % {"max": societe.max_utilisateurs})
        else:
            d = form.cleaned_data
            try:
                with schema_context(get_public_schema_name()), transaction.atomic():
                    adresse = Adresse.objects.create(
                        rue=d["rue"], numero=d["numero"], code_postal=d["code_postal"],
                        ville=d["ville"], pays=d["pays"],
                    )
                    utilisateur = Utilisateur.objects.create_user(
                        email=d["email"],
                        password=d["password"],
                        nom=d["nom"],
                        prenom=d["prenom"],
                        role=d["role"],
                        telephone=d.get("telephone") or None,
                        email_entreprise=d.get("email_entreprise") or None,
                        date_naissance=d.get("date_naissance") or None,
                        numero_compte_bancaire=d.get("numero_compte_bancaire") or None,
                        societe=societe,
                        schema_name=societe.schema_name,
                        adresse=adresse,
                    )
                _log(request, f"Création utilisateur {utilisateur.email} – tenant {societe.nom}")
                messages.success(request, _("Utilisateur créé pour %(nom)s.") % {"nom": societe.nom})
                if "ajouter_autre" in request.POST:
                    return redirect("utilisateurs:tenant_utilisateur_creer", pk=societe.pk)
                return redirect("utilisateurs:tenant_detail", pk=societe.pk)
            except Exception as e:
                messages.error(request, _("Erreur : %(erreur)s") % {"erreur": e})

    return render(request, "utilisateurs/tenants/tenant_utilisateur_form.html", {
        "form": form,
        "societe": societe,
    })


# ==================================================================
# ACTIVER / DÉSACTIVER UN UTILISATEUR
# ==================================================================
@login_required
@user_passes_test(is_admin)
def tenant_utilisateur_activer(request, pk, utilisateur_id):
    societe = get_object_or_404(_tenants(), pk=pk)
    if request.method == "POST":
        utilisateur = get_object_or_404(Utilisateur, pk=utilisateur_id, societe=societe)
        if not utilisateur.is_active and societe.nb_actifs >= societe.max_utilisateurs:
            messages.error(request, _("Le nombre maximum d'utilisateurs de ce tenant est atteint (%(max)s).")
                           % {"max": societe.max_utilisateurs})
        elif utilisateur.pk == request.user.pk:
            messages.error(request, _("Vous ne pouvez pas désactiver votre propre compte."))
        else:
            Utilisateur.objects.filter(pk=utilisateur.pk).update(is_active=not utilisateur.is_active)
            etat = _("activé") if not utilisateur.is_active else _("désactivé")
            _log(request, f"Utilisateur {utilisateur.email} {etat} – tenant {societe.nom}")
            messages.success(request, _("Utilisateur %(email)s %(etat)s.") % {"email": utilisateur.email, "etat": etat})
    return redirect("utilisateurs:tenant_detail", pk=societe.pk)
