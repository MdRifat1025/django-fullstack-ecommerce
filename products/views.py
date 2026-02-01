from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404
from  carousel.models import Carousel
from django.core.paginator import Paginator

from django.core.paginator import Paginator

def home(request):
    products = Product.objects.all().order_by('-created_at')
    carousel_items = Carousel.objects.all()

    # Search
    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)

    # Pagination
    paginator = Paginator(products, 4)  # 4 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,   # ✅ IMPORTANT
        'carousel': carousel_items,
        'page_obj': page_obj
    }
    return render(request, 'products/home.html', context)


def product_detail(request, slug):
    product=get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})

