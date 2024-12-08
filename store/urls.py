from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.all_categories, name='all_categories'),
    path('search/', views.search_results, name='search_results'),
    path('cart/', views.cart_detail, name='cart_detail'),  
    path('cart/add/<int:item_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('category/<slug:slug>/', views.category_items, name='category_items'),
    path('item/<slug:slug>/', views.item_detail, name='item_detail'),
]
