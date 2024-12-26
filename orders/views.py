from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import CartForm, AddCartForm
from .cart import Cart
from literature.models import Book
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem


class CartView(View):
    template_name = 'orders/cart.html'
    form_class = CartForm

    def get(self, request):
        form = CartForm()
        cart = Cart(request)

        context = {
            'form': form,
            'cart': cart
        }

        return render(request, self.template_name, context)


class CartAddView(View):
    form_class = AddCartForm

    def post(self, request, book_id):
        cart = Cart(request)
        book = get_object_or_404(Book, id=book_id)

        cart.add(book)
        return redirect('literature:book_detail', book.id)


class CartRemoveView(View):
    def get(self, request, book_id):
        cart = Cart(request)
        book = get_object_or_404(Book, id=book_id)
        cart.remove(book)

        return redirect('orders:cart')


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                book=item['book'],
                price=item['price'],
                quantity=item['quantity']
            )
        cart.clear()
        return redirect('orders:order_detail', order.id)


class OrderDetailView(LoginRequiredMixin, View):
    template_name = 'orders/order_detail.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, self.template_name, context={'order':order})

