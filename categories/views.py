from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from .models import Collection
from items.models import Item, Activity
from .forms import CollectionForm, ItemCollectionForm

# Create your views here.
class CollectionListView(ListView):
    model = Collection
    template_name = 'items/collection_list.html'
    context_object_name = 'collections'
    
    def get_queryset(self):
        search_text = self.request.GET.get('search', '')
        if search_text:
            return Collection.objects.filter(name__icontains=search_text)
        return Collection.objects.all()


class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'items/collection_detail.html'
    context_object_name = 'collection'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.filter(collection=self.object)
        return context


class CollectionCreateView(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'items/collection_create.html'
    success_url = reverse_lazy('collection_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f"Collection '{self.object.name}' created successfully!")
        return response


class CollectionUpdateView(LoginRequiredMixin, UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'items/collection_update.html'
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
    template_name = 'items/collection_delete.html'
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
    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        form = ItemCollectionForm(user=request.user, initial={'collection': item.collection})
        return render(request, 'items/add_to_collection.html', {'item': item, 'form': form})
    
    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        form = ItemCollectionForm(request.POST, user=request.user)
        
        if form.is_valid():
            old_collection = item.collection
            new_collection = form.cleaned_data['collection']
            item.collection = new_collection
            item.save()
            

            if new_collection:
                Activity.objects.create(
                    user=request.user,
                    item=item,
                    activity_type='add_to_collection'
                )
                messages.success(request, f"Item '{item.name}' added to collection '{new_collection.name}'!")
            else:
                if old_collection:
                    Activity.objects.create(
                        user=request.user,
                        item=item,
                        activity_type='remove_from_collection'
                    )
                    messages.success(request, f"Item '{item.name}' removed from collection!")
            
        
            return redirect('item_detail', id=item_id)
        
        return render(request, 'items/add_to_collection.html', {'item': item, 'form': form})


class RemoveFromCollectionView(LoginRequiredMixin, View):
    def post(self, request, item_id, collection_id):
        item = get_object_or_404(Item, id=item_id)
        collection = get_object_or_404(Collection, id=collection_id)
        
        if collection.user != request.user:
            messages.error(request, "You don't have permission to modify this collection.")
            return redirect('collection_detail', pk=collection_id)
        
        if item.collection == collection:
            item.collection = None
            item.save()
            
            Activity.objects.create(
                user=request.user,
                item=item,
                activity_type='remove_from_collection'
            )
            
            messages.success(request, f"Item '{item.name}' removed from collection '{collection.name}'!")
        
        return redirect('collection_detail', pk=collection_id)