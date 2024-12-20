from django.urls import path
from . import views

app_name = 'literature'
urlpatterns = [
    path('authors/', views.AuthorsView.as_view(), name='authors'),
    path('author_detail/<int:author_id>/', views.AuthorDetailView.as_view(), name='author_detail'),
]