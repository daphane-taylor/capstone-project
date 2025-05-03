from . import views
from django.urls import path

urlpatterns = [
	path('', views.HomeView.as_view(), name='root'),
	path('home/', views.HomeView.as_view(), name='home'),
	path('about/', views.AboutView.as_view(), name='about'),
	path('contact/', views.ContactView.as_view(), name='contact'),
]