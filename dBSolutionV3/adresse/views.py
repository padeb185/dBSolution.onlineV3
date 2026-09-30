# adresse/views.py
from core.suppression import analyser_suppression
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError, RestrictedError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from utilisateurs.models import UserLog
from .forms import AdresseForm
from adresse.models import Adresse
from django.utils.translation import gettext as _, gettext_noop
from .models import Adresse
from societe.models import Societe


@method_decorator([login_required, never_cache], name='dispatch')
class AdresseListView(ListView):
    model = Adresse
    template_name = "adresse/adresse_list.html"
    context_object_name = "adresses"
    ordering = ["rue"]

    def get_queryset(self):
        societe = self.request.user.societe
        return Adresse.objects.filter(societe=societe)



@never_cache
@login_required
def adresse_detail(request, adresse_id):
    tenant = request.user.societe


    adresse = get_object_or_404(
        Adresse,
        id=adresse_id,
        societe=tenant
    )


    return render(
        request,
        "adresse/adresse_detail.html",
        {
            "adresse": adresse,
        },
    )




@login_required
def ajouter_adresse_all(request):

    tenant = request.user.societe

    if request.method == "POST":

        form = AdresseForm(
            request.POST,
            societe=tenant,
        )

        if form.is_valid():

            try:
                adresse = form.save()

                messages.success(
                    request,
                    _(
                        "Adresse '%(rue)s, %(code_postal)s' ajoutée avec succès !"
                    ) % {
                        "rue": adresse.rue,
                        "code_postal": adresse.code_postal,
                    }
                )

                return redirect(
                    f"{reverse('adresse:adresse_list')}?saved=1"
                )


            except IntegrityError:
                messages.error(
                    request,
                    _("Cette adresse existe déjà.")
                )

            except ValidationError as e:
                messages.error(
                    request,
                    str(e)
                )

    else:

        form = AdresseForm(
            societe=tenant,
        )

    return render(
        request,
        "adresse/adresse_form.html",
        {
            "form": form,
            "tenant": tenant,
        }
    )






@login_required
def modifier_adresse(request, adresse_id):
    tenant = request.user.societe


    adresse = get_object_or_404(
        Adresse,
        id=adresse_id,
        societe=tenant
    )

    if request.method == "POST":
        form = AdresseForm(request.POST, instance=adresse)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                _("Adresse '%(rue)s, %(cp)s' modifiée avec succès !") % {
                    "rue": adresse.rue,
                    "cp": adresse.code_postal
                }
            )
            return redirect(
                f"{reverse('adresse:adresse_detail', kwargs={'adresse_id': adresse.id})}?saved=1"
            )
    else:
        form = AdresseForm(instance=adresse)

    return render(
        request,
        "adresse/modifier_adresse.html",
        {
            "form": form,
            "adresse": adresse,
        }
    )



ACTION_SUPPRESSION_ADRESSE = gettext_noop("Suppression de l'adresse")


@login_required
def delete_adresse_view(request, pk):
    adresse = get_object_or_404(Adresse.objects.select_related("societe"), pk=pk)

    analyse = analyser_suppression(adresse)
    # Une adresse ne doit jamais entraîner la suppression d'un client / fournisseur :
    # on bloque si elle est utilisée par un objet qui serait supprimé en cascade.
    utilisations = analyse["bloquants"] + analyse["supprimes"]
    objets_modifies = analyse["modifies"]
    suppression_possible = not utilisations

    if request.method == "POST":
        if not suppression_possible:
            messages.error(
                request,
                _("Impossible de supprimer cette adresse : elle est encore utilisée."),
            )
            return redirect("adresse:delete_adresse", pk=pk)

        libelle = str(adresse)

        # Libellé pour le log (capturé AVANT la suppression)
        ligne1 = f"{adresse.rue} {adresse.numero}" + (f" bte {adresse.boite}" if adresse.boite else "")
        nom_log = f"{ligne1}, {adresse.code_postal} {adresse.ville} ({adresse.code_pays})"
        nb_detaches = sum(len(objets) for _label, objets in objets_modifies)
        if nb_detaches:
            nom_log += f" – {nb_detaches} élément(s) détaché(s)"

        try:
            with transaction.atomic():
                adresse.delete()

                UserLog.objects.create(
                    utilisateur=request.user,
                    action=f"{ACTION_SUPPRESSION_ADRESSE} : {nom_log}",
                )
        except (ProtectedError, RestrictedError):
            messages.error(
                request,
                _("Impossible de supprimer cette adresse : elle est encore utilisée."),
            )
            return redirect("adresse:delete_adresse", pk=pk)

        messages.success(request, _("L'adresse « %(adresse)s » a bien été supprimée.") % {"adresse": libelle})
        return redirect("adresse:adresse_list")

    return render(
        request,
        "adresse/delete_adresse.html",
        {
            "adresse": adresse,
            "utilisations": utilisations,
            "objets_modifies": objets_modifies,
            "suppression_possible": suppression_possible,
        },
    )