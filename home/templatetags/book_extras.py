from django import template
from literature.models import Book

register = template.Library()


@register.simple_tag
def get_latest_books_in_category(category_name, limit=6):
    return Book.objects.filter(category__name=category_name).order_by('-created_at')[:limit]


@register.filter
def chunk(categories, chunk_size):
    chunk_size = int(chunk_size)
    return [categories[i:i + chunk_size] for i in range(0, len(categories), chunk_size)]