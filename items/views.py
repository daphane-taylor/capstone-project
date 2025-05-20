from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Item, CollectionComment, Activity
from .forms import ItemForm
from categories.models import Collection
from categories.forms import ItemCollectionForm, RemoveFromCollectionForm
from django.db.models import Q


class ItemListView(ListView):
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'
    #ordering = ['-created_on']

    def get_queryset(self):
        search_text = self.request.GET.get('search', '')
        if search_text:
            if self.request.user.is_authenticated:
                return Item.objects.filter(name__icontains=search_text, collections__user=self.request.user).distinct().order_by('id')
            return Item.objects.none()
        else:
            if self.request.user.is_authenticated:
                return Item.objects.filter(collections__user=self.request.user).distinct().order_by('id')
            return Item.objects.none()
        

class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = CollectionComment.objects.filter(item=self.object)
        
        if self.request.user.is_authenticated:
            user_collections = Collection.objects.filter(user=self.request.user)
            context['user_collections'] = user_collections
            
            item_collections = self.object.collections.all()
            context['item_collections'] = item_collections
            
            add_form = ItemCollectionForm(user=self.request.user, item=self.object)
            context['add_to_collection_form'] = add_form
            
            remove_form = RemoveFromCollectionForm(item=self.object)
            context['remove_from_collection_form'] = remove_form
        
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        
        if request.user.is_authenticated:
            Activity.objects.create(
                user=request.user,
                item=self.object,
                activity_type='view'
            )
            
        return response


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_create.html'
    success_url = reverse_lazy('item_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        item = self.object
        
        selected_collections = form.cleaned_data.get('collections', [])
        for collection in selected_collections:
            if not item.collections.filter(id=collection.id).exists():
                item.collections.add(collection)
                Activity.objects.create(
                    user=self.request.user,
                    item=item,
                    activity_type='add_to_collection',
                    collection=collection
                )
        
        Activity.objects.create(
            user=self.request.user,
            item=item,
            activity_type='create'
        )
        
        messages.success(self.request, f"Item '{item.name}' created successfully!")
        return response


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_update.html'
    pk_url_kwarg = 'id'
    context_object_name = 'item'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        return reverse('item_detail', kwargs={'id': self.object.id})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        item = self.object
        
        old_collections = set(item.collections.all())
        new_collections = set(form.cleaned_data.get('collections', []))
        
        for collection in new_collections - old_collections:
            item.collections.add(collection)
            Activity.objects.create(
                user=self.request.user,
                item=item,
                activity_type='add_to_collection',
                collection=collection
            )
        
        for collection in old_collections - new_collections:
            item.collections.remove(collection)
            Activity.objects.create(
                user=self.request.user,
                item=item,
                activity_type='remove_from_collection',
                collection=collection
            )
        
        messages.success(self.request, f"Item '{self.object.name}' updated successfully!")
        return response


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'items/item_delete.html'
    success_url = reverse_lazy('item_list')
    pk_url_kwarg = 'id'
    context_object_name = 'item'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        item_name = self.object.name
        
        if request.user.is_authenticated:
            Activity.objects.create(
                user=request.user,
                item=self.object,
                activity_type='delete'
            )
            
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"Item '{item_name}' deleted successfully!")
        return redirect(success_url)


class CreateCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        content = request.POST.get('content')
        item_id = request.POST.get('item_id')
        user = request.user

        item = get_object_or_404(Item, id=item_id)
        comment = CollectionComment.objects.create(
            item=item,
            content=content,
            author=user
        )
        comment.save()

        return redirect('item_detail', id=item_id)