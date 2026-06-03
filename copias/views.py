from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import CopiaChaveForm
from .models import CopiaChave


class CopiasChaveView(ListView):
    model = CopiaChave
    template_name = 'copias_chave.html'
    paginate_by = 8

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset().select_related('chave__sala__predio')
        if buscar:
            return qs.filter(chave__sala__predio__endereco__icontains=buscar)
        return qs


class CopiaChaveCreateView(SuccessMessageMixin, CreateView):
    model = CopiaChave
    form_class = CopiaChaveForm
    template_name = 'copia_chave_form.html'
    success_url = reverse_lazy('copias_chave')
    success_message = 'Copia de chave cadastrada com sucesso!'


class CopiaChaveUpdateView(SuccessMessageMixin, UpdateView):
    model = CopiaChave
    form_class = CopiaChaveForm
    template_name = 'copia_chave_form.html'
    success_url = reverse_lazy('copias_chave')
    success_message = 'Copia de chave alterada com sucesso!'


class CopiaChaveDeleteView(DeleteView):
    model = CopiaChave
    template_name = 'copia_chave_confirm_delete.html'
    success_url = reverse_lazy('copias_chave')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Copia de chave apagada com sucesso!')
        return super().delete(request, *args, **kwargs)

# Create your views here.
