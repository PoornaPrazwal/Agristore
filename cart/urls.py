from django.urls import path
from .views import add_to_cart, view_cart, remove_from_cart, update_cart_item, success

urlpatterns = [
    path("add-to-cart/", add_to_cart, name="add_to_cart"),
    path("cart/", view_cart, name="view_cart"),
    path("remove-from-cart/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path('update-cart-item/<int:item_id>/<str:action>/', update_cart_item, name='update_cart_item'),
    path('success/',success,name='success'),

]
