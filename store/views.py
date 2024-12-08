from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Category, Item
from .cart import Cart
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q

def index(request):
    items = Item.objects.all()  # Get all items
    context = {
        'items': items
    }
    return render(request, 'store/index.html', context)

def search_results(request):
    query = request.GET.get('query', '')
    items = Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'store/partials/product_list.html', {'items': items})

def category_items(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = Item.objects.filter(category=category)
    return render(request, 'store/category_items.html', {'category': category, 'items': items})

def item_detail(request, slug):
    item = get_object_or_404(Item, slug=slug)
    return render(request, 'store/item_detail.html', {'item': item})

def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'store/all_categories.html', {'categories': categories,})

# Cart Views
def cart_detail(request):
    cart = Cart(request)  # Initialize the cart
    return render(request, 'store/cart.html', {'cart': cart})  # Pass the cart to the template

def cart_add(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.add(item)
    return redirect('cart_detail')

def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return redirect('cart_detail')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Ensure 'index' is a valid URL name
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'store/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})
