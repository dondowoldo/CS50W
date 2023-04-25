from .models import Listing, User
from django import forms
from django.forms import ModelForm

class CreateListing(ModelForm):
    class Meta:
        model = Listing
        fields = ("name", "price", "description", "imageurl", "category")
        labels = {"name":'',
                "price": '',
                "description": '',
                "imageurl": '',
                "category": 'Select at least one category. (To select multiple, hold CTRL)'}
        widgets = {
            "name": forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Title'}),
            "price": forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Starting Bid'}),
            "description": forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Describe your listing here', 'style':'resize:none;'}),
            "imageurl": forms.URLInput(attrs={'class':'form-control', 'placeholder': 'Paste Image URL here'}),
            "category": forms.SelectMultiple(attrs={'class':'form-control'})
        }