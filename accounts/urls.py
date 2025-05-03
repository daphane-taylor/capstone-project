
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password_form.html'), name='password_change'),
]