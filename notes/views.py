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

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Note, NoteActivity
from django.urls import reverse_lazy
from .forms import NoteForm

# Create your views here.
class NotesList(ListView):
    model = Note
    template_name = 'notes/list.html'
    context_object_name = 'note_list'
    ordering = ['-created_on']
	



class NotesDetail(DetailView):
    model = Note
    template_name = 'notes/detail.html'
    context_object_name = 'note'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note'] = self.object
        return context
    
    def get(self, request, *args, **kwargs):    
        response = super().get(request, *args, **kwargs)
        
        # Only track view activity if the user is authenticated
        if request.user.is_authenticated:
            NoteActivity.objects.create(
                user=request.user,
                note=self.object,
                activity_type='view'
            )
            
        return response

class NotesCreate(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'notes/create.html'
    form_class = NoteForm
    success_url = reverse_lazy('note_list')  # instead of reverse_lazy('/notes/list/')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        # Create activity record after the note is saved
        NoteActivity.objects.create(
            user=self.request.user,
            note=self.object,
            activity_type='create'
        )
        
        return response

class NotesUpdate(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = 'notes/update.html'
    fields = ['title', 'content', 'image']
    
    def get_success_url(self):
        return reverse_lazy('note_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class NotesDelete(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/delete.html'
    success_url = reverse_lazy('note_list')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Record delete activity before deleting the note
        if request.user.is_authenticated:
            NoteActivity.objects.create(
                user=request.user,
                note=self.object,
                activity_type='delete'
            )
            
        return super().post(request, *args, **kwargs)