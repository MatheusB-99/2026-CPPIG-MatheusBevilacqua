
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('alterar-senha/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html', success_url=reverse_lazy('password_change_done')), name='alterar_senha'),
    path('alterar-senha/ok/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('usuarios/', include('usuarios.urls')),
    path('predios/', include('predios.urls')),
    path('salas/', include('salas.urls')),
    path('chaves/', include('chaves.urls')),
    path('copias/', include('copias.urls')),
    path('reservas/', include('reservas.urls')),
    path('emprestimos/', include('emprestimos.urls')),
    path('', include('home.urls')),
]
