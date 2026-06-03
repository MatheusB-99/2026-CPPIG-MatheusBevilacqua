from django.urls import path

from .views import CopiasChaveView, CopiaChaveCreateView, CopiaChaveDeleteView,  CopiaChaveUpdateView

urlpatterns = [
    path('', CopiasChaveView.as_view(), name='copias_chave'),
    path('nova/', CopiaChaveCreateView.as_view(), name='copia_chave_nova'),
    path('<int:pk>/editar/', CopiaChaveUpdateView.as_view(), name='copia_chave_editar'),
    path('<int:pk>/excluir/', CopiaChaveDeleteView.as_view(), name='copia_chave_excluir'),
]