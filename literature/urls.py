from django.urls import path
from . import views

app_name = 'literature'
urlpatterns = [
    path('authors/', views.AuthorsView.as_view(), name='authors'),
    path('author_detail/<int:author_id>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('publishers/', views.PublisherView.as_view(), name='publishers'),
    path('publisher_detail/<int:publisher_id>/', views.PublisherDetailView.as_view(), name='publisher_detail'),

    path('translators/', views.TranslatorsView.as_view(), name='translators'),
    path('translator_detail/<int:translator_id>/', views.TranslatorDetailView.as_view(), name='translator_detail'),

]