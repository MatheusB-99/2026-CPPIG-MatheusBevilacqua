from django.urls import path

from .views import UsuarioCreateView, UsuarioDeleteView, UsuarioListView, UsuarioUpdateView


urlpatterns = [
    path('', UsuarioListView.as_view(), name='usuarios'),
    path('novo/', UsuarioCreateView.as_view(), name='usuario_novo'),
    path('<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuario_editar'),
    path('<int:pk>/excluir/', UsuarioDeleteView.as_view(), name='usuario_excluir'),
]