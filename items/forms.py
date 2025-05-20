from django import forms
from .models import Item
from categories.models import Collection

class ItemForm(forms.ModelForm):
    collections = forms.ModelMultipleChoiceField(
        queryset=Collection.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Item
        fields = ['name', 'other_names', 'date_collected', 'value', 'vendor', 'color', 'type', 'size', 'description', 'image']
        widgets = {
            'date_collected': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['collections'].queryset = Collection.objects.filter(user=user)
            
            if self.instance and self.instance.pk:
                self.initial['collections'] = self.instance.collections.all()