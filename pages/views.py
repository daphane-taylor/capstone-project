from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from itertools import chain
from operator import attrgetter
from items.models import Activity as ItemActivity, Item
from notes.models import NoteActivity, Note
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib import messages

class HomeView(TemplateView):
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            # Import here to avoid circular import
            from categories.models import Collection
            
            item_activities = ItemActivity.objects.select_related('user', 'item').filter(user=self.request.user)[:10]
            note_activities = NoteActivity.objects.select_related('user', 'note').filter(user=self.request.user)[:10]
            
            combined_activities = sorted(
                chain(item_activities, note_activities),
                key=attrgetter('timestamp'),
                reverse=True
            )[:30]
            
            context['total_items'] = Item.objects.filter(collections__user=self.request.user).distinct().count()
            context['total_notes'] = Note.objects.filter(user=self.request.user).count()
            context['total_collections'] = Collection.objects.filter(user=self.request.user).count()
            context['recent_activities'] = combined_activities
        else:
            context['total_items'] = 0
            context['total_notes'] = 0
            context['total_collections'] = 0
            context['recent_activities'] = []
            
        return context
    
class AboutView(TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ContactView(TemplateView):
    template_name = 'pages/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', ContactForm())
        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Save the contact message to database
            contact_message = form.save()
            
            # Extract form data for email
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data.get('phone', '')
            extension = form.cleaned_data.get('extension', '')
            phone_type = form.cleaned_data.get('phone_type', '')
            subject = form.cleaned_data['subject']
            message_text = form.cleaned_data['message']
            
            message_body = f"""
            Contact Form Submission
            
            From: {name}
            Email: {email}
            Phone: {phone} {extension} ({phone_type})
            
            Message:
            {message_text}
            """
            
            try:
                send_mail(
                    f'Contact Form: {subject}',
                    message_body,
                    email,  # From email
                    ['daphane.elizabeth@gmail.com'],  # To email
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent successfully!")
                return redirect('contact')
            except Exception as e:
                messages.error(request, f"There was an error sending your message: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
            
        # If we got here, there was an error - pass the form back to the template
        kwargs['form'] = form
        return self.get(request, *args, **kwargs)