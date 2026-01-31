from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404
from  carousel.models import Carousel

def home(request):
    products = Product.objects.all().order_by('-created_at')
    carousel_items = Carousel.objects.all()  # renamed for clarity

    context = {
        'products': products,
        'carousel': carousel_items,
    }

    return render(request, 'products/home.html', context)

def product_detail(request, slug):
    product=get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})

