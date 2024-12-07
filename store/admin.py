from django.contrib import admin
from .models import Category, Item, UserProfile, Cart, CartItem

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
