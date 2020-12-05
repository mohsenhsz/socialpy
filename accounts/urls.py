from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.UserLogin, name='login'),
    path('logout/', views.UserLogout, name='logout'),
    path('register/', views.UserRegister, name='register'),
    path('profile/<int:user_id>/', views.UserProfile, name='profile'),
    path('edit_profile/<int:user_id>/', views.EditProfile, name='edit_profile'),
    path('follow/', views.Follow, name='follow'),
    path('unfollow/', views.Unfollow, name='unfollow'),
    path('phone_login/', views.PhoneLogin, name='phone_login'),
    path('verify/', views.VerifyPhone, name='verify_phone'),
]
