from .models import Listing, User, Bid
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
                "category": 'Select a category.(Optional), Hold down CTRL to select more than one'}
        widgets = {
            "name": forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Title'}),
            "price": forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Starting Bid'}),
            "description": forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Describe your listing here', 'style':'resize:none;'}),
            "imageurl": forms.URLInput(attrs={'class':'form-control', 'placeholder': 'Paste Image URL here (Optional)'}),
            "category": forms.SelectMultiple(attrs={'class':'form-control'})
        }

class PlaceBid(ModelForm):
    class Meta:
        model = Bid
        fields = ("price",)
        labels = {"price": '',}
        
        widgets = {
            "price": forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Place Bid'})
        }