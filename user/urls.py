from django.urls import path
from .views import LoginClass, Register, logoutPage, UpdateProfile, ChangePassword, ForgotPassword

app_name='user'
urlpatterns = [
    path('Login/', LoginClass.as_view(), name='login'),
    path('Signup/',Register.as_view(),name='register'),
    path('logout/',logoutPage,name='logout'),
    path('update/',UpdateProfile.as_view(), name='update'),
    path('update_profile/',UpdateProfile.as_view(), name='update_profile'),
    path('change_password/',ChangePassword.as_view(),name='change_password'),
    path('forgot_password/',ForgotPassword.as_view(), name='forgot_password'),

]