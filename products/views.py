from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404

def home(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request,'products/home.html', {'products': products})

def product_detail(request, slug):
    product=get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})