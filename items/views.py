"""
Class-based views:

View        = generic view
ListView    = get a list of records
DetailView  = get a single(detail) record
CreateView  = create a new record
DeleteView  = remove a record
UpdateView  = modify an existing record
LoginView   = login
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Item, CollectionComment, Activity
from .forms import ItemForm


class ItemListView(ListView):
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'
    ordering = ['-created_on']

    def get_queryset(self):
        search_text = self.request.GET.get('search', '')
        if search_text:
            # Filter notes based on the search text
            return Item.objects.filter(name__icontains=search_text)
        
        else:
			# Filter notes by the logged-in user
            return Item.objects.all()


class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = CollectionComment.objects.filter(item=self.object)
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        
        # Only track view activity if the user is authenticated
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
    
    def form_valid(self, form):
        response = super().form_valid(form)
        item = self.object
        
        # Record activity for new item creation
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
    
    def get_success_url(self):
        return reverse('item_detail', kwargs={'id': self.object.id})
    
    def form_valid(self, form):
        response = super().form_valid(form)
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
        
        # Record delete activity before deleting the item
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