from django.urls import path

from .views import ChaveCreateView, ChaveDeleteView, ChavesView, ChaveUpdateView

urlpatterns = [
    path('', ChavesView.as_view(), name='chaves'),
    path('nova/', ChaveCreateView.as_view(), name='chave_nova'),
    path('<int:pk>/editar/', ChaveUpdateView.as_view(), name='chave_editar'),
    path('<int:pk>/excluir/', ChaveDeleteView.as_view(), name='chave_excluir'),
]