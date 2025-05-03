from django.urls import path
from . import views

urlpatterns = [
    path('', views.ItemListView.as_view(), name='item_list'),
    path('create/', views.ItemCreateView.as_view(), name='item_create'),
    path('<int:id>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('<int:id>/update/', views.ItemUpdateView.as_view(), name='item_update'),
    path('<int:id>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
    path('create_comment/', views.CreateCommentView.as_view(), name='create_comment'),
]