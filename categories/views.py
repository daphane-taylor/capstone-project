from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Collection
from items.models import Item
from .forms import CollectionForm
from django.contrib import messages

# Create your views here.
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
            return Collection.objects.filter(user=self.request.user).prefetch_related('items')
        return Collection.objects.none()


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