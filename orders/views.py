from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests

@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('view_cart')

    total = sum(item.get_total_price() for item in cart_items)

    # Create Order
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        status='Pending'
    )

    # Create Order Items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.new_price
        )

    # Cart clear
    cart_items.delete()

    return redirect('payment_init', order_id=order.id)

    

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})




def payment_init(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    ssl_url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"

    post_data = {
        'store_id': settings.SSLC_STORE_ID,
        'store_passwd': settings.SSLC_STORE_PASS,
        'total_amount': order.total_amount,
        'currency': "BDT",
        'tran_id': f"ORDER_{order.id}",
        'success_url': request.build_absolute_uri('/orders/payment-success/'),
        'fail_url': request.build_absolute_uri('/orders/payment-fail/'),
        'cancel_url': request.build_absolute_uri('/orders/payment-cancel/'),
        'cus_name': request.user.username,
        'cus_email': request.user.email,
        'cus_phone': "01700000000",
        'cus_add1': "Dhaka",
        'cus_city': "Dhaka",
        'cus_country': "Bangladesh",
        'shipping_method': "NO",
        'product_name': "Ecommerce Order",
        'product_category': "General",
        'product_profile': "general",
    }

    response = requests.post(ssl_url, data=post_data)
    response_data = response.json()

    if response_data.get('status') == 'SUCCESS':
        return redirect(response_data['GatewayPageURL'])
    else:
        return redirect('payment_fail')




@csrf_exempt
def payment_success(request):
    tran_id = request.POST.get('tran_id')
    if not tran_id:
        return redirect('order_history')

    order_id = tran_id.replace("ORDER_", "")
    order = Order.objects.get(id=order_id)

    # prevent double update
    if order.status != "Paid":
        order.status = "Paid"
        order.save()

        # reduce stock
        for item in order.items.all():   # related_name='items'
            product = item.product
            product.stock -= item.quantity
            product.save()

    return redirect('order_history')



@csrf_exempt
def payment_fail(request):
    tran_id = request.POST.get('tran_id')
    if not tran_id:
        return redirect('order_history')

    order_id = tran_id.replace("ORDER_", "")
    order = Order.objects.get(id=order_id)
    order.status = "Failed"
    order.save()
    return redirect('order_history')



@csrf_exempt
def payment_cancel(request):
    return redirect('order_history')

