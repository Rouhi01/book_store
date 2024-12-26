from literature.models import Category
from orders.cart import Cart


def categories(request):
    categories = Category.objects.all()
    size = (len(categories) + 1) // 2
    return {'categories': categories, 'size':size}


def cart(request):
    return {'cart': Cart(request)}