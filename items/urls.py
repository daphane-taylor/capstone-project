from . import views
from django.urls import path

urlpatterns = [
	path('', views.item_list_view, name='item_list'),
	path('create/', views.item_create_view, name='item_create'),
	path('<int:id>/', views.item_detail_view, name='item_detail'),
	path('<int:id>/update/', views.item_update_view, name='item_update'),
	path('<int:id>/delete/', views.item_delete_view, name='item_delete'),
]