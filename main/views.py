from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MenuItem, Cart, CartItem
from .forms import UserProfileForm  
from django.contrib.auth.models import User

def home(request):
    return render(request, 'main/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('menu')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def menu(request):
    if not request.user.is_authenticated:
        return redirect('login')
    query = request.GET.get('q')
    if query:
        menu_items = MenuItem.objects.filter(name__icontains=query)
    else:
        menu_items = MenuItem.objects.all()
    return render(request, 'main/menu.html', {'menu_items': menu_items})


def add_to_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')
    menu_item = get_object_or_404(MenuItem, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
    cart_item.price = menu_item.price * cart_item.quantity
    cart_item.save()
    cart.update_total() 
    return redirect('menu')


def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'main/view_cart.html', {'cart_items': cart_items , 'cart': cart})


def adjust_quantity(request, item_id, action):
    if not request.user.is_authenticated:
        return redirect('login')
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.price = cart_item.menu_item.price * cart_item.quantity
    cart_item.save()
    cart_item.cart.update_total() 
    return redirect('view_cart')


def remove_item(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
    cart_item.delete()
    cart_item.cart.update_total()
    return redirect('view_cart')


def confirm_order(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if cart_items.exists():
        for item in cart_items:
            item.is_confirmed = True
            item.save()
        messages.success(request, 'Order confirmed successfully!')
    else:
        messages.error(request, 'Your cart is empty.')
    return redirect('order_confirmation')


def order_confirmation(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart_items = CartItem.objects.filter(cart__user=request.user, is_confirmed=True).order_by('-created_at')
    cart = Cart.objects.get(user=request.user)
    return render(request, 'main/order_confirmation.html', {'cart_items': cart_items, 'cart': cart})


def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = CartItem.objects.filter(cart__user=request.user, is_confirmed=True).order_by('-created_at')
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('user_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'main/user_profile.html', {'form': form, 'orders': orders})


