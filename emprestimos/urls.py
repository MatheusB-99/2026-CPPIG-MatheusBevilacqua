from django.urls import path

from .views import EmprestimoCreateView, EmprestimoDeleteView, EmprestimosView, EmprestimoUpdateView


urlpatterns = [
    path('', EmprestimosView.as_view(), name='emprestimos'),
    path('novo/', EmprestimoCreateView.as_view(), name='emprestimo_novo'),
    path('<int:pk>/editar/', EmprestimoUpdateView.as_view(), name='emprestimo_editar'),
    path('<int:pk>/excluir/', EmprestimoDeleteView.as_view(), name='emprestimo_excluir'),
]