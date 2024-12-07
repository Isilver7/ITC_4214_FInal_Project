from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Item
from .cart import Cart

def index(request):
    categories = Category.objects.all()[:5]  # Get first 5 categories
    items = Item.objects.all()[:5]           # Get first 5 items
    context = {
        'categories': categories,
        'items': items
    }
    return render(request, 'store/index.html', context)

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

def login(request):
    return render(request, 'store/login.html')
