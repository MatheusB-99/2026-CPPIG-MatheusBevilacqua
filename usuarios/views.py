from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import UsuarioForm
from .models import Usuario


class UsuarioListView(ListView):
    model = Usuario
    template_name = 'usuarios.html'
    paginate_by = 8

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()
        if buscar:
            return qs.filter(
                Q(nome__icontains=buscar)
                | Q(email__icontains=buscar)
                | Q(cpf__icontains=buscar)
            )
        return qs


class UsuarioCreateView(SuccessMessageMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario_form.html'
    success_url = reverse_lazy('usuarios')
    success_message = 'Usuario cadastrado com sucesso!'


class UsuarioUpdateView(SuccessMessageMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario_form.html'
    success_url = reverse_lazy('usuarios')
    success_message = 'Usuario alterado com sucesso!'


class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'usuario_confirm_delete.html'
    success_url = reverse_lazy('usuarios')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Usuario apagado com sucesso!')
        return super().delete(request, *args, **kwargs)
