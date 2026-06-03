from django.urls import path

from .views import PredioCreateView, PredioDeleteView, PrediosView, PredioUpdateView

urlpatterns = [
    path('', PrediosView.as_view(), name='predios'),
    path('novo/', PredioCreateView.as_view(), name='predio_novo'),
    path('<int:pk>/editar/', PredioUpdateView.as_view(), name='predio_editar'),
    path('<int:pk>/excluir/', PredioDeleteView.as_view(), name='predio_excluir'),
]