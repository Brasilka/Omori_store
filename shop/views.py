from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Category, Product, Order
from .forms import CustomUserRegistrationForm, CustomLoginForm, OrderForm
from decimal import Decimal

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'categories': categories, 'products': products})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    return render(request, 'shop/category_detail.html', {'category': category, 'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal(0)

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        cart_items.append({'product': product, 'quantity': quantity, 'total': float(product.price * quantity)})
        total_price += product.price * quantity

    request.session['cart_total'] = float(total_price)
    return render(request, 'shop/cart_detail.html', {'cart_items': cart_items, 'total_price': float(total_price)})

def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_detail')

def cart_update(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart_detail')

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'shop/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = CustomLoginForm()
    return render(request, 'shop/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = request.session.get('cart_total', 0)
            order.save()
            cart = request.session.get('cart', {})
            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                order.products.add(product)
            request.session['cart'] = {}
            return redirect('order_history')
    else:
        form = OrderForm()
    return render(request, 'shop/order_form.html', {'form': form})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_history.html', {'orders': orders})
