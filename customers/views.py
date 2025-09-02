from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib import messages
from .forms import CustomerFarmerRegistrationForm, FarmerCropForm
from .models import Profile
from farmers.models import FarmerCrop, Crop
from cart.models import Cart, CartItem
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request,'index.html')

from django.contrib.auth import authenticate, login

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(username,password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) 
            if user.is_superuser:
                return redirect('admin:index')
            else:
                profile = Profile.objects.get(user=user)
                if profile.user_type == "customer":
                    return redirect("customer_home")
                elif profile.user_type == "farmer":
                    return redirect("farmer_home")
        else:
            messages.error(request, "Invalid username or password")
    return render(request,'login.html')

def register_user(request):
    if request.method == 'POST':
        form = CustomerFarmerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful")
            return redirect('login') 
    else:
        form = CustomerFarmerRegistrationForm()
    print(form)
    return render(request, 'registration.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('index')

def customer_home(request):
    search_query = request.GET.get('search', '').strip()  # Get search query from URL

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all() # Assuming you have a Cart instance
    cart_items_count = cart_items.count()  # Get the total number of items
    cart_crop_ids = cart_items.values_list('crop_id', flat=True)  # Extract crop IDs

    print(f"Cart Items Count: {cart_items_count}")

    print(f"Cart Crop IDs: {cart_crop_ids}")
    farmer_crops = FarmerCrop.objects.filter(is_available=True, quantity__gte=1)
    # .exclude(id__in=cart_crop_ids)
    if search_query:
        farmer_crops = farmer_crops.filter(
            Q(crop__name__icontains=search_query) |  # Search by crop name
            Q(farmer__user__username__icontains=search_query) & # Search by farmer username
            ~Q(id__in=cart_crop_ids)  # Exclude crops already in cart
        )
    
    print(farmer_crops)

    return render(
            request,
            "C-home.html",
            {  
                "farmer_crops": farmer_crops,
                "cart_items": cart_crop_ids,
                "search_query": search_query,
            },
        )
   