# tips/forms.py
# Responsibility: Dhruv Patel

from django import forms
from .models import RecyclingTip, TipCategory

class RecyclingTipForm(forms.ModelForm):
    class Meta:
        model = RecyclingTip
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tip title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Share your recycling tip...'}),
        }