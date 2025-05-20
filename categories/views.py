from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Collection
from items.models import Item, Activity
from .forms import CollectionForm, ItemCollectionForm
from django.contrib import messages


class CollectionListView(ListView):
    model = Collection
    template_name = 'categories/collection_list.html'
    context_object_name = 'collections'
    
    def get_queryset(self):
        search_text = self.request.GET.get('search', '')
        if search_text:
            if self.request.user.is_authenticated:
                return Collection.objects.filter(name__icontains=search_text, user=self.request.user)
            return Collection.objects.none()
        if self.request.user.is_authenticated:
            return Collection.objects.filter(user=self.request.user)
        return Collection.objects.none()
    

class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'categories/collection_detail.html'
    context_object_name = 'collection'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Collection.objects.filter(user=self.request.user)
        return Collection.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add items related to this collection to the context
        context['items'] = self.object.items.all()
        return context


class CollectionCreateView(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'categories/collection_create.html'
    success_url = reverse_lazy('collection_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f"Collection '{self.object.name}' created successfully!")
        return response


class CollectionUpdateView(LoginRequiredMixin, UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'categories/collection_update.html'
    context_object_name = 'collection'
    
    def get_success_url(self):
        return reverse('collection_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Collection '{self.object.name}' updated successfully!")
        return response
    
    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)


class CollectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Collection
    template_name = 'categories/collection_delete.html'
    success_url = reverse_lazy('collection_list')
    context_object_name = 'collection'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        collection_name = self.object.name
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"Collection '{collection_name}' deleted successfully!")
        return redirect(success_url)
    
    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)


class AddToCollectionView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        collection_id = request.POST.get('collection')
        
        if collection_id:
            collection = get_object_or_404(Collection, id=collection_id, user=request.user)
            
            if not item.collections.filter(id=collection.id).exists():
                item.collections.add(collection)
                
                Activity.objects.create(
                    user=request.user,
                    item=item,
                    activity_type='add_to_collection',
                    collection=collection
                )
                
                messages.success(request, f"Added '{item.name}' to collection '{collection.name}'")
            else:
                messages.info(request, f"'{item.name}' is already in collection '{collection.name}'")
                
        return redirect('item_detail', id=item_id)


class RemoveFromCollectionView(LoginRequiredMixin, View):
    def post(self, request, item_id, collection_id=None):
        item = get_object_or_404(Item, id=item_id)
        
        
        if collection_id:
            collection = get_object_or_404(Collection, id=collection_id, user=request.user)
            collections_to_remove = [collection]
        else:
            selected_collection_id = request.POST.get('collection')
            if selected_collection_id:
                collection = get_object_or_404(Collection, id=selected_collection_id, user=request.user)
                collections_to_remove = [collection]
            else:
                messages.error(request, "No collection selected")
                return redirect('item_detail', id=item_id)
        
        for collection in collections_to_remove:
            if item.collections.filter(id=collection.id).exists():
                item.collections.remove(collection)
                
                Activity.objects.create(
                    user=request.user,
                    item=item,
                    activity_type='remove_from_collection',
                    collection=collection
                )
                
                messages.success(request, f"Removed '{item.name}' from collection '{collection.name}'")
        
        return redirect('item_detail', id=item_id)