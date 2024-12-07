from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.all_categories, name='all_categories'),
    path('cart/', views.cart_detail, name='cart_detail'),  # Updated to point to the correct cart detail view
    path('cart/add/<int:item_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('login/', views.login, name='login'),
    path('category/<slug:slug>/', views.category_items, name='category_items'),
    path('item/<slug:slug>/', views.item_detail, name='item_detail'),
]
