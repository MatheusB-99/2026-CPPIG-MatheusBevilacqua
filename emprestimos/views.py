from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import EmprestimoForm
from .models import Emprestimo


class EmprestimosView(ListView):
    model = Emprestimo
    template_name = 'emprestimos.html'
    paginate_by = 8

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset().select_related('usuario', 'copia_chave', 'reserva')
        if buscar:
            return qs.filter(usuario__nome__icontains=buscar)
        return qs


class EmprestimoCreateView(SuccessMessageMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Emprestimo cadastrado com sucesso!'


class EmprestimoUpdateView(SuccessMessageMixin, UpdateView):
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Emprestimo alterado com sucesso!'


class EmprestimoDeleteView(DeleteView):
    model = Emprestimo
    template_name = 'emprestimo_confirm_delete.html'
    success_url = reverse_lazy('emprestimos')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Emprestimo apagado com sucesso!')
        return super().delete(request, *args, **kwargs)
