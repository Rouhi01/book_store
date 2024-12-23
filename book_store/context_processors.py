from literature.models import Category


def categories(request):
    categories = Category.objects.all()
    size = (len(categories) + 1) // 2
    return {'categories': categories, 'size':size}