# items/forms.py
from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'other_names', 'date_collected', 'value', 'color', 'type', 'size', 'description', 'collections', 'image']
        widgets = {
            'date_collected': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'collections':  forms.SelectMultiple(attrs={'class': 'form-control'}),
        }