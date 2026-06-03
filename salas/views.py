from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import SalaForm
from .models import Sala, SalaComunitaria, SalaExclusiva


class SalasView(ListView):
    model = Sala
    template_name = 'salas.html'
    paginate_by = 8

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset().select_related('predio')
        if buscar:
            return qs.filter(predio__endereco__icontains=buscar)
        return qs


class SalaTipoMixin:
    def _sincronizar_tipo_sala(self, sala, tipo_sala):
        SalaComunitaria.objects.filter(pk=sala.pk).delete()
        SalaExclusiva.objects.filter(pk=sala.pk).delete()
        if tipo_sala == Sala.TipoSala.COMUNITARIA:
            SalaComunitaria.objects.create(sala_ptr_id=sala.pk, predio=sala.predio)
        elif tipo_sala == Sala.TipoSala.EXCLUSIVA:
            SalaExclusiva.objects.create(sala_ptr_id=sala.pk, predio=sala.predio)


class SalaCreateView(SuccessMessageMixin, SalaTipoMixin, CreateView):
    model = Sala
    form_class = SalaForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala cadastrada com sucesso!'

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        self._sincronizar_tipo_sala(self.object, form.cleaned_data.get('tipo_sala'))
        return response


class SalaUpdateView(SuccessMessageMixin, SalaTipoMixin, UpdateView):
    model = Sala
    form_class = SalaForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala alterada com sucesso!'

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        self._sincronizar_tipo_sala(self.object, form.cleaned_data['tipo_sala'])
        return response


class SalaDeleteView(DeleteView):
    model = Sala
    template_name = 'sala_confirm_delete.html'
    success_url = reverse_lazy('salas')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Sala apagada com sucesso!')
        return super().delete(request, *args, **kwargs)

# Create your views here.
