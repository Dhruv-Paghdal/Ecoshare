# items/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Item, ItemImage, Category

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'condition', 'location', 'is_free', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Neighborhood, etc.'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Allows uploading multiple images on the same page as the item
ItemImageFormSet = inlineformset_factory(
    Item,
    ItemImage,
    form=ItemImageForm,
    extra=3,
    max_num=5,
    can_delete=True
)