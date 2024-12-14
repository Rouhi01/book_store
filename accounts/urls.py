from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('signup/message_send_email', views.MessageSendEmailView.as_view(), name='message_send_email'),
    path('signup/finally/<uidb64>/<token>', views.SignUpFinallyView.as_view(), name='signup_finally'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('bio/', views.BioView.as_view(), name='bio'),
]