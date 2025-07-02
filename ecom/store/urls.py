
from django.contrib import admin
# from django.conf.urls.static import static

from django.urls import path
# from django.conf import settings
from . import views

urlpatterns = [
  path('admin/',admin.site.urls),
  path('',views.home),
  path('men/',views.men),
  path('women/',views.women),
  path('contact/',views.contact),
  path('register/',views.register), 
  path('about/',views.about),
  path('user_about/',views.user_about),
  path('login/',views.login),
  path('userhome/',views.userhome),
  path('user_mobile/',views.user_mobile),
  path('user_women/',views.user_women),
  path('user_men/',views.user_men),
  path('verify/', views.verify),
  path('forget_p/',views.forget_p),
  path('mobile/',views.mobile),
  path('manage_order/', views.manage_order),
  path('manageuserstatus/', views.manageuserstatus),
  path('address/',views.address),
  path('place_order/', views.place_order, name='place_order'),
  # path('profile_view/',views.profile_view),
  path('profile/',views.profile),
  path('edit_profile/',views.edit_profile),
  path('detail/<slug:slug>/',views.detail),
  path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
  path('cart-count/', views.cart_count, name='cart_count'),
  path('checkout/', views.checkout, name='checkout'),
  path('cart/', views.view_cart, name='view_cart'),
  path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  
  path('my_order/', views.my_order),
  # path('payment-success/', views.payment_success, name='payment_success'),
  # path('place_order/', views.place_order, name='place_order'),
  path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
  path('order_list/', views.order_list),
  path('epuser/', views.epuser),
  path('cpuser/', views.cpuser),
  

]