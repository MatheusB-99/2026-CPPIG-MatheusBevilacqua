from django.views.generic import TemplateView

from chaves.models import Chave
from copias.models import CopiaChave
from predios.models import Predio
from reservas.models import Reserva
from salas.models import Sala


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_predios'] = Predio.objects.count()
        context['total_salas'] = Sala.objects.count()
        context['total_chaves'] = Chave.objects.count()
        context['total_copias'] = CopiaChave.objects.count()
        context['total_reservas'] = Reserva.objects.count()
        return context