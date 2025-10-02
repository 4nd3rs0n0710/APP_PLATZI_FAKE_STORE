# Configuración de URLs del Proyecto (plattistore/urls.py)
from django.contrib import admin
from django.urls import path, include

# No necesitamos importar vistas específicas aquí si usamos `include`
# from accounts.views import register_view, login_view 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. URLs de la aplicación 'products'
    path('', include('products.urls')),
    
    # 2. URLs de la aplicación 'accounts'
    # Esto incluye tus vistas personalizadas (como /register/ y /login/)
    # ya que tu comentario anterior indica: path('', include('accounts.urls'))
    path('', include('accounts.urls')), 
    
    # 3. MÓDULO DE RESTABLECIMIENTO DE CONTRASEÑA DE DJANGO AUTH
    # Incluimos `django.contrib.auth.urls` BAJO el namespace 'accounts'.
    # Esto es VITAL para que los patrones de password reset (como password_reset_confirm)
    # se llamen correctamente desde la plantilla de correo como 'accounts:password_reset_confirm'.
    # Usamos el prefijo 'accounts/' para todas estas URLs por convención.
    path('accounts/', include('django.contrib.auth.urls')),
]
