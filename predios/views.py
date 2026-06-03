from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import PredioForm
from .models import Predio


class PrediosView(ListView):
    model = Predio
    template_name = 'predios.html'
    paginate_by = 8

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()
        if buscar:
            return qs.filter(endereco__icontains=buscar)
        return qs


class PredioCreateView(SuccessMessageMixin, CreateView):
    model = Predio
    form_class = PredioForm
    template_name = 'predio_form.html'
    success_url = reverse_lazy('predios')
    success_message = 'Predio cadastrado com sucesso!'


class PredioUpdateView(SuccessMessageMixin, UpdateView):
    model = Predio
    form_class = PredioForm
    template_name = 'predio_form.html'
    success_url = reverse_lazy('predios')
    success_message = 'Predio alterado com sucesso!'


class PredioDeleteView(DeleteView):
    model = Predio
    template_name = 'predio_confirm_delete.html'
    success_url = reverse_lazy('predios')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Predio apagado com sucesso!')
        return super().delete(request, *args, **kwargs)

# Create your views here.
