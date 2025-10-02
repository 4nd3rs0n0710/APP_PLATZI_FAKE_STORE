# accounts/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

app_name = 'accounts'

urlpatterns = [
    # --- VISTAS DE API (Endpoints para JavaScript) ---
    path('api/register/', views.register_api, name='api_register'),
    path('api/login/', views.login_api, name='api_login'),
    path('api/logout/', views.logout_api, name='api_logout'),
    path('api/profile/', views.user_profile_api, name='api_profile'),
    path('api/check-username/', views.check_username_api, name='api_check_username'),
    
    # --- VISTAS DEL NAVEGADOR (Login, Register, Logout) ---
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # --- VISTAS DE RESTABLECIMIENTO DE CONTRASEÑA (Django Auth Views) ---
    # NOTA: Estas URLs requieren que crees las plantillas asociadas.
    
    # 1. Formulario para solicitar el email: name='password_reset' (Soluciona el NoReverseMatch)
    path('password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), 
        name='password_reset'
    ),
    
    # 2. Confirmación de que el email ha sido enviado: name='password_reset_done'
    path('password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), 
        name='password_reset_done'
    ),
    
    # 3. Enlace con token para establecer la nueva contraseña: name='password_reset_confirm'
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), 
        name='password_reset_confirm'
    ),
    
    # 4. Mensaje de confirmación final: name='password_reset_complete'
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), 
        name='password_reset_complete'
    ),
]
