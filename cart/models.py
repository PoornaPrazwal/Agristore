from django.db import models
from django.contrib.auth.models import User
from farmers.models import  FarmerCrop
from django.utils import timezone


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total(self):
        total = sum(item.get_total_price() for item in self.items.all())
        return total

# CartItem model: represents an item in the cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    crop = models.ForeignKey(FarmerCrop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}kg {self.crop.name} in cart"

    def get_total_price(self):
        return self.crop.price_per_kg * self.quantity



class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_signature = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=False)
    ordered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.customer.username}"

    
    def get_total(self):
        return sum(order_item.get_total_price() for order_item in self.order_items.all())




class OrderItem(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('on_the_way', 'On The Way'),
        ('delivered', 'Delivered'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    crop = models.ForeignKey(FarmerCrop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='accepted')

   

    def __str__(self):
        return f"{self.quantity} x {self.crop}"

    def get_total_price(self):
        return self.crop.price_per_kg * self.quantity


    
 