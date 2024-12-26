from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:book_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:book_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),

]