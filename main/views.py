from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CustomUser, Product, SoldProduct, BuyerInfo
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


def vegetables(request):
    products = Product.objects.filter(product_type='vegetable').all()
    context = {
        'products': products
    }
    return render(request, 'vegetables.html', context)


def fruits(request):
    products = Product.objects.filter(product_type='fruits').all()
    context = {
        'products': products
    }
    return render(request, 'fruits.html', context)


def product_detail(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)


def register_user(request):

    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in')
        return redirect('index')

    if request.method == 'POST':
        first_name = request.POST['firstName']
        email = request.POST['emailAddress']
        phone_number = request.POST['phoneNumber']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']

        if password == confirm_password:
            try:
                user = CustomUser.objects.create_user(email=email, first_name=first_name, phone_number=phone_number, password=password)
                user.save()
                messages.success(request, 'User registered successfully')
                return redirect('index')
            except:
                messages.error(request, 'User with this email already exists')
                return render(request, 'register.html')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            messages.error(request, 'User not found')
            return render(request, 'login.html')
        else:
            if user.check_password(password):
                messages.success(request, 'Login successful')
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid password')
                return render(request, 'login.html')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect("index")


@login_required(login_url="/login")
def buy_product(request):
    if request.method == "POST":
        product_id = request.POST.get("productId")
        category = request.POST.get("category")
        quantity = request.POST.get("quantity")
        address = request.POST.get("address")
        user = request.user

        if category and product_id:
            try:
                product = get_object_or_404(Product, id=product_id)
                sold_product = SoldProduct.objects.create(product=product, category=category, quantity=quantity, address=address, buyer=user)
                return redirect("orders")
            except Exception as err:
                print(err)
                messages.error(request, "Something is wrong...")
                return redirect("index")
        return redirect("index")

@login_required(login_url="/login")
def orders(request):
    orders = SoldProduct.objects.filter(buyer=request.user).all().order_by('-date_sold')
    return render(request, "orders.html", {"orders": orders})


@login_required(login_url="/login")
def profile(request):
    return render(request, 'profile.html')


def about(request):
    return render(request, "about.html")