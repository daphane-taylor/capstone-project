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
        required=True,
        empty_label="Select a Collection"
    )

    def __init__(self, *args, user=None, item=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            user_collections = Collection.objects.filter(user=user)
            
            if item:
                item_collections = item.collections.all()
                self.fields['collection'].queryset = user_collections.exclude(id__in=[c.id for c in item_collections])
            else:
                self.fields['collection'].queryset = user_collections

class RemoveFromCollectionForm(forms.Form):
    collection = forms.ModelChoiceField(
        queryset=Collection.objects.none(),
        required=True,
        empty_label="Select a Collection"
    )

    def __init__(self, *args, item=None, **kwargs):
        super().__init__(*args, **kwargs)
        if item:
            # Only show collections that the item is in
            self.fields['collection'].queryset = item.collections.all()