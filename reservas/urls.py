from django.urls import path

from .views import ReservaCreateView, ReservaDeleteView, ReservasView, ReservaUpdateView

urlpatterns = [
    path('', ReservasView.as_view(), name='reservas'),
    path('nova/', ReservaCreateView.as_view(), name='reserva_nova'),
    path('<int:pk>/editar/', ReservaUpdateView.as_view(), name='reserva_editar'),
    path('<int:pk>/excluir/', ReservaDeleteView.as_view(), name='reserva_excluir'),
]