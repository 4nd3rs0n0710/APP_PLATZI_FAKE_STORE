from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name="product_list"),
    path('create/', views.product_create, name="product_create"),
    path('product/<int:product_id>/', views.product_detail, name="product_detail"),        # ← / agregado
    path('product/<int:product_id>/edit/', views.edit_product, name="edit_product"),       # ← / agregado
    path('product/<int:product_id>/delete/', views.delete_product, name="delete_product"), # ← / agregado
]