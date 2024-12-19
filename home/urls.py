from django.urls import path
from home import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # path('like/<str:model_name>/<int:object_id>/<str:parent_model_name>/<int:parent_object_id>/', views.LikeCommentView.as_view(), name='like_comment'),
    path('like/<str:model_name>/<int:object_id>/', views.LikeView.as_view(), name='like'),

    path('like/<int:user_id>/<str:model_name>/<int:object_id>/', views.CommentView.as_view(), name='comment'),
    path('like/<int:user_id>/<str:model_name>/<int:object_id>/<int:comment_id>/', views.CommentReplyView.as_view(), name='comment_reply'),
]
app_name = 'home'
