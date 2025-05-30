from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('signup/message_send_email', views.MessageSendEmailView.as_view(), name='message_send_email'),
    path('signup/finally/<uidb64>/<token>', views.SignUpFinallyView.as_view(), name='signup_finally'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),

    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('edit_profile/<int:user_id>/', views.EditProfileView.as_view(), name='edit_profile'),

    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', views.UnFollowView.as_view(), name='unfollow'),

    path('post_detail/<int:user_id>/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail')
]