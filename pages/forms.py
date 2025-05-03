from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'extension', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
            'phone': forms.TextInput(attrs={'placeholder': 'Optional'}),
            'extension': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }