from django.urls import path
from .views import (
	CollectionListView, 
	CollectionDetailView,
	CollectionCreateView, 
	CollectionUpdateView, 
	CollectionDeleteView,
	AddToCollectionView, 
	RemoveFromCollectionView
)

urlpatterns = [
    path('', CollectionListView.as_view(), name='collection_list'),
    path('<int:pk>/', CollectionDetailView.as_view(), name='collection_detail'),
    path('create/', CollectionCreateView.as_view(), name='collection_create'),
    path('<int:pk>/update/', CollectionUpdateView.as_view(), name='collection_update'),
    path('<int:pk>/delete/', CollectionDeleteView.as_view(), name='collection_delete'),
    path('items/<int:item_id>/add-to-collection/', AddToCollectionView.as_view(), name='add_to_collection'),
    path('items/<int:item_id>/remove-from-collection/<int:collection_id>/', RemoveFromCollectionView.as_view(), name='remove_from_collection'),
    path('items/<int:item_id>/remove-from-collection/', RemoveFromCollectionView.as_view(), name='remove_from_collection_form'),
]