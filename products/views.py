from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests

# Endpoints de la API
API_URL_PRODUCTS = "https://api.escuelajs.co/api/v1/products"
API_URL_CATEGORIES = "https://api.escuelajs.co/api/v1/categories"


# Vista para mostrar productos
def product_list(request):
    try:
        response = requests.get(API_URL_PRODUCTS)
        response.raise_for_status()
        products = response.json()
    except requests.exceptions.RequestException:
        products = []
    return render(request, "product_list.html", {"products": products})

# Vista para crear producto
def create_product(request):
    # Obtener categorías desde la API
    try:
        response = requests.get(API_URL_CATEGORIES)
        response.raise_for_status()
        categories = response.json()
    except requests.exceptions.RequestException:
        categories = []

    if request.method == "POST":
        data = {
            "title": request.POST["title"],
            "price": int(request.POST["price"]),
            "description": request.POST["description"],
            "categoryId": int(request.POST["categoryId"]),
            "images": [request.POST["image"]]
        }
        try:
            response = requests.post(API_URL_PRODUCTS, json=data)
            if response.status_code == 201:
                return redirect("product_list")
            else:
                return HttpResponse("❌ Error al crear producto", status=400)
        except requests.exceptions.RequestException:
            return HttpResponse("❌ No se pudo conectar con la API", status=500)
        
    return render(request, "create_product.html", {"categories": categories})
