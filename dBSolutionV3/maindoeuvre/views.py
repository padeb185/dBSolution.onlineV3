from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy

from utilisateurs.models import MainDoeuvre
from utilisateurs.forms import MainDoeuvreForm


class MainDoeuvreListView(ListView):
    model = MainDoeuvre
    template_name = "main_oeuvre/list.html"
    context_object_name = "main_oeuvres"


class MainDoeuvreCreateView(CreateView):
    model = MainDoeuvre
    form_class = MainDoeuvreForm
    template_name = "main_oeuvre/form.html"
    success_url = reverse_lazy("main_oeuvre_list")

    def form_valid(self, form):
        return super().form_valid(form)


class MainDoeuvreUpdateView(UpdateView):
    model = MainDoeuvre
    form_class = MainDoeuvreForm
    template_name = "main_oeuvre/form.html"
    success_url = reverse_lazy("main_oeuvre_list")


class MainDoeuvreDeleteView(DeleteView):
    model = MainDoeuvre
    template_name = "main_oeuvre/confirm_delete.html"
    success_url = reverse_lazy("main_oeuvre_list")