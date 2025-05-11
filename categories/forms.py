from .models import Collection
from items.models import Item
from django import forms

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ItemCollectionForm(forms.Form):
    collection = forms.ModelChoiceField(
        queryset=Collection.objects.none(),
        required=False,
        empty_label="No Collection"
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['collections'].queryset = Collection.objects.filter(user=user)