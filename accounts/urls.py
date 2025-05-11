from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html',next_page='home'), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password_form.html',success_url='/accounts/password_change/done/'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/change_password_done.html'), name='password_change_done'),
    path('update_profile/', views.ProfileUpdate.as_view(), name='update_profile'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
]