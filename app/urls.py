from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('', views.HomeView.as_view(), name='home'),
    path('eventos', views.EventoListView.as_view(), name='evento-list'),
    path('eventos/nova/', views.EventoCreateView.as_view(), name='evento-create'),
    path('eventos/<int:pk>/editar/', views.EventoUpdateView.as_view(), name='evento-update'),
    path('eventos/<int:pk>/excluir/', views.EventoDeleteView.as_view(), name='evento-delete'),
    path('inscrever/<int:evento_id>/', views.InscricaoCreateView.as_view(), name='inscrever'),
    path('desinscrever/<int:pk>/', views.InscricaoDeleteView.as_view(), name='desinscrever'),
    path('perfil/participante', views.ParticipanteListView.as_view(), name='perfil-participante'),
    path('perfil/participante/<int:pk>/editar/', views.ParticipanteUpdateView.as_view(), name='perfil-participante-update'),
    path('perfil/participante/<int:pk>/excluir/', views.ParticipanteDeleteView.as_view(), name='perfil-participante-delete'),
    path('perfil/organizador', views.OrganizadorListView.as_view(), name='perfil-organizador'),
    path('perfil/organizador/<int:pk>/editar', views.OrganizadorUpdateView.as_view(), name='perfil-organizador-update'),
    path('perfil/organizador/<int:pk>/excluir/', views.OrganizadorDeleteView.as_view(), name='perfil-organizador-delete'),
    path('perfil/usuario/<int:pk>/editar', views.UserUpdateView.as_view(), name='perfil-usuario-update'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registro/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registro/password_change_done_form.html'), name='password_change_done'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard')
]

from .views import ParticipanteSignUpView, OrganizadorSignUpView

urlpatterns += [
    path('signup/participante/', ParticipanteSignUpView.as_view(), name='signup_participante'),
    path('signup/organizador/', OrganizadorSignUpView.as_view(), name='signup_organizador'),
]

from django.contrib.auth.views import LoginView, LogoutView

urlpatterns += [
    path('login/', LoginView.as_view(template_name='registro/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]