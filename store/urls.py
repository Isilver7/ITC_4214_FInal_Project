from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

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
    path('profile/', views.profile_view, name='profile'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('rate/<int:item_id>/', views.rate_item, name='rate_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('about-us/', views.about_us, name='about_us'),
]
