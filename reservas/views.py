from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

from .forms import ReservaForm
from .models import Reserva


class ReservasView(ListView):
    model = Reserva
    template_name = 'reservas.html'
    paginate_by = 8

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset().select_related('usuario', 'copia_chave')
        if buscar:
            return qs.filter(usuario__nome__icontains=buscar)
        return qs


class ReservaEmailMixin:
    def _get_reserva_email_data(self, reserva):
        email = [reserva.usuario.email]
        descricao = []
        if reserva.copia_chave and reserva.copia_chave.chave:
            chave = reserva.copia_chave.chave
            descricao.append(f'Chave: {chave}')
            if chave.tipo == 'sala' and chave.sala:
                descricao.append(f'Sala: {chave.sala}')
            elif chave.tipo == 'predio' and chave.predio:
                descricao.append(f'Prédio: {chave.predio}')

        dados = {
            'cliente': reserva.usuario.nome,
            'email': reserva.usuario.email,
            'id_reserva': reserva.id,
            'data_inicio': reserva.data_inicio.strftime('%d/%m/%Y') if reserva.data_inicio else '',
            'horario_inicio': reserva.horario_inicio.strftime('%H:%M') if reserva.horario_inicio else '',
            'data_fim': reserva.data_fim.strftime('%d/%m/%Y') if reserva.data_fim else '',
            'horario_fim': reserva.horario_fim.strftime('%H:%M') if reserva.horario_fim else '',
            'copia_chave': str(reserva.copia_chave) if reserva.copia_chave else 'N/A',
            'status': reserva.get_status_display(),
            'descricao': descricao,
        }
        return email, dados

    def _send_reserva_email(self, subject, reserva):
        email, dados = self._get_reserva_email_data(reserva)
        texto_email = render_to_string(template_name='emails/texto_email.txt', context=dados)
        html_email = render_to_string(template_name='emails/texto_email.html', context=dados)

        send_mail(
            subject=subject,
            message=texto_email,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=email,
            html_message=html_email,
            fail_silently=False,
        )


class ReservaCreateView(ReservaEmailMixin, SuccessMessageMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva cadastrada com sucesso!'

    def form_valid(self, form):
        response = super().form_valid(form)
        reserva = self.object
        try:
            self._send_reserva_email('Confirmação de Reserva - ChaveMaster', reserva)
        except Exception:
            pass
        return response


class ReservaUpdateView(ReservaEmailMixin, SuccessMessageMixin, UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva alterada com sucesso!'

    def form_valid(self, form):
        response = super().form_valid(form)
        reserva = self.object
        try:
            self._send_reserva_email('Reserva Atualizada - ChaveMaster', reserva)
        except Exception:
            pass
        return response


class ReservaDeleteView(ReservaEmailMixin, DeleteView):
    model = Reserva
    template_name = 'reserva_confirm_delete.html'
    success_url = reverse_lazy('reservas')

    def delete(self, request, *args, **kwargs):
        reserva = self.get_object()
        try:
            self._send_reserva_email('Reserva Cancelada - ChaveMaster', reserva)
        except Exception:
            pass
        messages.success(request, 'Reserva apagada com sucesso!')
        return super().delete(request, *args, **kwargs)
