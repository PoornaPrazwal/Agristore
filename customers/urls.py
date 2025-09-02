from django.urls import path
from .views import index,login_user,register_user,logout_user,customer_home
urlpatterns = [
    path('', index,name='index'),
    path('login/',login_user,name='login'),
    path('register/',register_user,name='register'),
    path('logout/',logout_user,name='logout'),
    path('customer_home/',customer_home,name='customer_home'),
]
