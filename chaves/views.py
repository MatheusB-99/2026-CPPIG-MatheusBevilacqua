from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import ChaveForm
from .models import Chave


class ChavesView(ListView):
    model = Chave
    template_name = 'chaves.html'
    paginate_by = 8

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset().select_related('sala__predio', 'predio')
        if buscar:
            return qs.filter(
                Q(sala__predio__endereco__icontains=buscar)
                | Q(predio__endereco__icontains=buscar)
            )
        return qs


class ChaveCreateView(SuccessMessageMixin, CreateView):
    model = Chave
    form_class = ChaveForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave cadastrada com sucesso!'


class ChaveUpdateView(SuccessMessageMixin, UpdateView):
    model = Chave
    form_class = ChaveForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave alterada com sucesso!'


class ChaveDeleteView(DeleteView):
    model = Chave
    template_name = 'chave_confirm_delete.html'
    success_url = reverse_lazy('chaves')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Chave apagada com sucesso!')
        return super().delete(request, *args, **kwargs)

# Create your views here.
