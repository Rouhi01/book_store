from django.urls import path
from home import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # path('like/<str:model_name>/<int:object_id>/<str:parent_model_name>/<int:parent_object_id>/', views.LikeCommentView.as_view(), name='like_comment'),
    path('like/<str:model_name>/<int:object_id>/', views.LikeView.as_view(), name='like'),

    path('comment/<int:user_id>/<str:model_name>/<int:object_id>/<str:app_name>/', views.CommentView.as_view(), name='comment'),
    path('comment/<int:user_id>/<str:model_name>/<int:object_id>/<int:comment_id>/<str:app_name>/', views.CommentReplyView.as_view(), name='comment_reply'),

    path('contact_us/', views.ContactUsView.as_view(), name='contact_us'),
    path('about_us/', views.AboutUsView.as_view(), name='about_us'),
]
app_name = 'home'
