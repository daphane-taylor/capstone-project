# Add these to items/urls.py
from django.urls import path
from .views import (CollectionListView, CollectionDetailView, 
    CollectionCreateView, CollectionUpdateView, CollectionDeleteView,
    AddToCollectionView, RemoveFromCollectionView
)

# Add these URL patterns to the existing urlpatterns list
path('collections/', CollectionListView.as_view(), name='collection_list'),
path('collections/<int:pk>/', CollectionDetailView.as_view(), name='collection_detail'),
path('collections/create/', CollectionCreateView.as_view(), name='collection_create'),
path('collections/<int:pk>/update/', CollectionUpdateView.as_view(), name='collection_update'),
path('collections/<int:pk>/delete/', CollectionDeleteView.as_view(), name='collection_delete'),
path('items/<int:item_id>/add-to-collection/', AddToCollectionView.as_view(), name='add_to_collection'),
path('items/<int:item_id>/remove-from-collection/<int:collection_id>/', RemoveFromCollectionView.as_view(), name='remove_from_collection'),