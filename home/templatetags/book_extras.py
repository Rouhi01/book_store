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


@register.filter
def render_stars(rate):
    full_stars = int(rate) // 2  # تعداد ستاره‌های کامل
    half_star = 1 if rate % 2 != 0 else 0  # اگر نیم‌ستاره نیاز است
    empty_stars = 5 - (full_stars + half_star)  # تعداد ستاره‌های خالی

    stars_html = '<i class="fas fa-star"></i>' * full_stars
    stars_html += '<i class="fas fa-star-half-alt"></i>' * half_star
    stars_html += '<i class="far fa-star"></i>' * empty_stars

    return stars_html