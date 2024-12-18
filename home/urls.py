from django.urls import path
from home import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('like/<str:model_name>/<int:object_id>/', views.LikeView.as_view(), name='like')
]