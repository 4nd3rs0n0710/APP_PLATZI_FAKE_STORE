from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests

API_URL = "https://api.escuelajs.co/api/v1/products"

# Vista para mostrar productos
def product_list(request):
    response = requests.get(API_URL)
    products = response.json()
    return render(request, "product_list.html", {"products": products})

# Vista para crear producto
def create_product(request):
    if request.method == "POST":
        data = {
            "title": request.POST["title"],
            "price": int(request.POST["price"]),
            "description": request.POST["description"],
            "categoryId": int(request.POST["categoryId"]),
            "images": [request.POST["image"]]
        }
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            return redirect("product_list")
        else:
            return HttpResponse("Error al crear producto", status=400)
    return render(request, "create_product.html")
