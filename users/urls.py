from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, email_verification, ResetPassword

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirm/<str:verification_code>/', email_verification, name='email-confirm'),
    path('reset/', ResetPassword.as_view(), name='reset'),
    path('profile/', ProfileView.as_view(), name='profile')
]