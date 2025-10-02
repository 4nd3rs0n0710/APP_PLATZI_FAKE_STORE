from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from .forms import ProductForm
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
        "products/product_list.html",
        {"products": products, "categories": categories},
    )

@login_required(login_url='accounts:login')
def product_create(request):
    # Define base_url si no está definida
    base_url = "https://api.escuelajs.co/api/v1/"  # ← AÑADE ESTA LÍNEA
    
    # 1. Obtener categorías desde la API
    try:
        resp_cat = requests.get(f'{base_url}categories/', timeout=10)
        resp_cat.raise_for_status()
        cats_json = resp_cat.json()
        # Transformar a lista (id, nombre)
        categories = [(c['id'], c['name']) for c in cats_json if c.get('id') and c.get('name')]
    except requests.RequestException:
        categories = []
        messages.error(request, 'Error al cargar las categorías.')

    if request.method == 'POST':
        form = ProductForm(request.POST, categories=categories)
        if form.is_valid():
            # 2. Construir el payload a enviar
            payload = {
                "title":       form.cleaned_data['title'],
                "price":       float(form.cleaned_data['price']),
                "description": form.cleaned_data['description'],
                "categoryId":  int(form.cleaned_data['category']),
                "images":      [form.cleaned_data['image']],
            }
            try:
                # 3. Consumo del endpoint POST
                headers = {'Content-Type': 'application/json'}
                
                # Si tenemos token en sesión, agregarlo
                if 'api_token' in request.session:
                    headers['Authorization'] = f'Bearer {request.session["api_token"]}'
                
                resp_post = requests.post(
                    f'{base_url}products/',
                    json=payload,
                    headers=headers,
                    timeout=10
                )
                resp_post.raise_for_status()
                
                # 4. Al crear con éxito, redirigir al listado
                product_data = resp_post.json()
                product_title = product_data.get('title', 'Producto')
                messages.success(request, f'✅ "{product_title}" ha sido creado exitosamente.')
                return redirect('products:product_list')
                
            except requests.RequestException as e:
                messages.error(request, 'Error al crear el producto en la API. Intenta nuevamente.')
                form.add_error(None, 'Error al crear el producto en la API')
    else:
        form = ProductForm(categories=categories)

    return render(request, 'products:product_create.html', {
        'form': form
    })

# 📌 Detalle de producto
def product_detail(request, product_id):
    try:
        response = requests.get(f"{API_URL_PRODUCTS}/{product_id}")
        response.raise_for_status()
        product = response.json()
    except requests.exceptions.RequestException:
        return HttpResponse("❌ Error al obtener el producto", status=500)

    return render(request, "products/product_detail.html", {"product": product})

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
            "images": [request.POST.get("image") or product.get("images", [""])[0]],
        }
        try:
            response = requests.put(f"{API_URL_PRODUCTS}/{product_id}", json=data)
            if response.status_code in [200, 201]:
                # 💡 CORRECCIÓN APLICADA AQUÍ: Se agregó 'products:' al nombre de la URL.
                return redirect("products:product_detail", product_id=product_id)
            return HttpResponse("❌ Error al actualizar producto", status=response.status_code)
        except requests.exceptions.RequestException:
            return HttpResponse("❌ No se pudo conectar con la API", status=500)

    return render(
        request,
        "products/edit_product.html",
        {"product": product, "categories": categories},
    )
# 📌 Eliminar producto
def delete_product(request, product_id):
    try:
        response = requests.delete(f"{API_URL_PRODUCTS}/{product_id}")
        if response.status_code == 200:
            return redirect("products:product_list")
        return HttpResponse("❌ Error al eliminar producto", status=response.status_code)
    except requests.exceptions.RequestException:
        return HttpResponse("❌ No se pudo conectar con la API", status=500)