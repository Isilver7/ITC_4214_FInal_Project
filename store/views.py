from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Category, Item, Profile, Rating
from .cart import Cart
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from .forms import ProfileForm, ItemUpdateForm
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    items = Item.objects.all()  
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
    
    recommended_items = Item.objects.filter(category=item.category).exclude(id=item.id)[:4]
    
    context = {
        'item': item,
        'recommended_items': recommended_items,
    }
    return render(request, 'store/item_detail.html', context)


def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'store/all_categories.html', {'categories': categories,})


def cart_detail(request):
    cart = Cart(request) 
    return render(request, 'store/cart.html', {'cart': cart})  

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
            return redirect('index')  
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


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        try:
            profile.name = request.POST.get('name')
            profile.surname = request.POST.get('surname')
            profile.age = request.POST.get('age')
            profile.preferred_size = request.POST.get('preferred_size')
            profile.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
            messages.error(request, "There was an error updating your profile.")
    return render(request, 'store/profile.html', {'profile': profile})


@login_required
@csrf_exempt
def rate_item(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            stars = int(data.get('stars', 0))
            if stars < 1 or stars > 5:
                return JsonResponse({'success': False, 'error': 'Invalid rating value.'}, status=400)
            
            item = Item.objects.get(id=item_id)
            rating, created = Rating.objects.get_or_create(item=item, user=request.user)
            rating.stars = stars
            rating.save()

            return JsonResponse({'success': True, 'stars': rating.stars})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found.'}, status=404)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid data format.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:  
        messages.error(request, "Your cart is empty. Add items to proceed to checkout.")
        return redirect('cart_detail')
    
   
    cart.clear()  
    messages.success(request, "Checkout successful! Thank you for your purchase.")
    return redirect('index')


def about_us(request):
    return render(request, 'store/about_us.html')

def is_staff(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_staff)
def manage_items(request):
    items = Item.objects.all()
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        item.price = request.POST.get('price')
        item.stock = request.POST.get('stock')
        item.save()
        messages.success(request, f"{item.name} updated successfully!")
        return redirect('manage_items')
    
    return render(request, 'store/manage_items.html', {
        'items': items,
    })
