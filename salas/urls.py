from django.urls import path

from .views import SalaCreateView, SalaDeleteView, SalasView, SalaUpdateView

urlpatterns = [
    path('', SalasView.as_view(), name='salas'),
    path('nova/', SalaCreateView.as_view(), name='sala_nova'),
    path('<int:pk>/editar/', SalaUpdateView.as_view(), name='sala_editar'),
    path('<int:pk>/excluir/', SalaDeleteView.as_view(), name='sala_excluir'),
]