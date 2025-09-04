from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests

# Endpoints de la API
API_URL_PRODUCTS = "https://api.escuelajs.co/api/v1/products"
API_URL_CATEGORIES = "https://api.escuelajs.co/api/v1/categories"


# 📌 Listar productos
def product_list(request):
    try:
        response = requests.get(API_URL_PRODUCTS)
        response.raise_for_status()
        products = response.json()
    except requests.exceptions.RequestException:
        products = []

    # Obtener categorías (para el filtro en el HTML)
    try:
        response = requests.get(API_URL_CATEGORIES)
        response.raise_for_status()
        categories = response.json()
    except requests.exceptions.RequestException:
        categories = []

    return render(
        request,
        "product_list.html",
        {"products": products, "categories": categories},
    )


# 📌 Crear producto
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
            "title": request.POST.get("title"),
            "price": int(request.POST.get("price", 0)),
            "description": request.POST.get("description"),
            "categoryId": int(request.POST.get("categoryId", 0)),
            "images": [request.POST.get("image")],
        }
        try:
            response = requests.post(API_URL_PRODUCTS, json=data)
            if response.status_code == 201:
                return redirect("product_list")
            else:
                return HttpResponse("❌ Error al crear producto", status=response.status_code)
        except requests.exceptions.RequestException:
            return HttpResponse("❌ No se pudo conectar con la API", status=500)

    return render(request, "create_product.html", {"categories": categories})


# 📌 Detalle de producto
def product_detail(request, product_id):
    try:
        response = requests.get(f"{API_URL_PRODUCTS}/{product_id}")
        response.raise_for_status()
        product = response.json()
    except requests.exceptions.RequestException:
        return HttpResponse("❌ Error al obtener el producto", status=500)

    return render(request, "product_detail.html", {"product": product})


# 📌 Editar producto
def edit_product(request, product_id):
    # Obtener producto
    try:
        response = requests.get(f"{API_URL_PRODUCTS}/{product_id}")
        response.raise_for_status()
        product = response.json()
    except requests.exceptions.RequestException:
        return HttpResponse("❌ Producto no encontrado", status=404)

    # Obtener categorías
    try:
        response = requests.get(API_URL_CATEGORIES)
        response.raise_for_status()
        categories = response.json()
    except requests.exceptions.RequestException:
        categories = []

    if request.method == "POST":
        data = {
            "title": request.POST.get("title"),
            "price": int(request.POST.get("price", 0)),
            "description": request.POST.get("description"),
            "categoryId": int(request.POST.get("categoryId", 0)),
            "images": [request.POST.get("image")],
        }
        try:
            response = requests.put(f"{API_URL_PRODUCTS}/{product_id}", json=data)
            if response.status_code in [200, 201]:
                return redirect("product_detail", product_id=product_id)
            else:
                return HttpResponse("❌ Error al actualizar producto", status=response.status_code)
        except requests.exceptions.RequestException:
            return HttpResponse("❌ No se pudo conectar con la API", status=500)

    return render(request, "edit_product.html", {"product": product, "categories": categories})


# 📌 Eliminar producto
def delete_product(request, product_id):
    try:
        response = requests.delete(f"{API_URL_PRODUCTS}/{product_id}")
        if response.status_code == 200:
            return redirect("product_list")
        else:
            return HttpResponse("❌ Error al eliminar producto", status=response.status_code)
    except requests.exceptions.RequestException:
        return HttpResponse("❌ No se pudo conectar con la API", status=500)
