from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from .models import Cart, CartItem, Order,OrderItem
from farmers.models import Crop,FarmerCrop
from django.contrib.auth.decorators import login_required
import razorpay

@login_required
def add_to_cart(request):
    if request.method == "POST":
        crop_id = request.POST.get("crop_id")
        quantity = int(request.POST.get("quantity", 1))

        crop = get_object_or_404(FarmerCrop, id=crop_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, crop=crop)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        
        cart_item.save()

        return JsonResponse({"success": True, "message": f"{quantity} kg of {crop.crop.name} added to cart! at {crop.price_per_kg}/kg","cartItemLength":cart.items.count()})

    return JsonResponse({"success": False, "message": "Invalid request."})


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.get_total()
    client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID, settings.RAZOR_PAY_KEY_SECRET)) 
    amount = int(total_price*100)

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        'razorpay_key': settings.RAZOR_PAY_KEY_ID,
        }

    if amount > 0:
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': 1}) 
        cart.order_id = payment['id']
        cart.save()
        context['payment'] = payment

    
    return render(request, "checkout.html", context)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect("view_cart")



def update_cart_item(request, item_id, action):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'User not authenticated'})

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
    farmer_crop = get_object_or_404(FarmerCrop, id=cart_item.crop.id)

    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement' and cart_item.quantity > 1:
        cart_item.quantity -= 1
  
    if cart_item.quantity > farmer_crop.quantity:
        messages.error(request, f"Quantity cannot be more than {farmer_crop.quantity} kg")
        cart_item.quantity = farmer_crop.quantity
    else:
        messages.success(request, "Cart updated successfully")


    cart_item.save()
    return JsonResponse({
        'success': True,
        'quantity': cart_item.quantity,
        'total_price': cart_item.get_total_price(),
        'cart_total':cart.get_total() ,
    })

def success(request):

    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    payment_signature = request.GET.get('signature')

    cart = get_object_or_404(Cart, order_id=order_id)
    cart.is_paid = True
    cart.save()

    order = Order.objects.create(
        customer=cart.user,
        order_id=order_id,
        payment_id=payment_id,
        payment_signature=payment_signature,
        status=True
    )
    order.save()
    
    for item in cart.items.all():
        OrderItem.objects.create(order=order, crop=item.crop, quantity=item.quantity)
        farmer_crop = get_object_or_404(FarmerCrop, id=item.crop.id)
        farmer_crop.quantity -= item.quantity

    clear_cart(cart)

    return render(request, 'payment_success.html', {'order_id': order_id})


def clear_cart(cart):
    cart.items.all().delete()
    cart.is_paid = False
    cart.order_id = None
    cart.save()
    return