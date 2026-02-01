from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get quantity from form (default 1)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except:
        quantity = 1

    # Prevent adding more than stock
    if quantity > product.stock:
        messages.error(request, f"Only {product.stock} items available in stock.")
        return redirect('view_cart')

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > product.stock:
            cart_item.quantity = product.stock
            messages.warning(request, f"Quantity adjusted to available stock ({product.stock})")
    else:
        cart_item.quantity = quantity

    cart_item.save()
    messages.success(request, f"{product.name} added to cart!")
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if request.method == "POST":
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except:
            quantity = 1

        if quantity > cart_item.product.stock:
            quantity = cart_item.product.stock
            messages.warning(request, f"Quantity adjusted to available stock ({cart_item.product.stock})")

        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"{cart_item.product.name} quantity updated!")

    return redirect('view_cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, f"{cart_item.product.name} removed from cart!")
    return redirect('view_cart')
