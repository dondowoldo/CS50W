from .models import Listing, Bid, Comment, Category
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

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("Starting bid has to be more than 0")
        return price

class PlaceBid(ModelForm):
    def __init__(self, maxprice, listing, *args, **kwargs):          ## passing in variable 'maxprice' from views
        super().__init__(*args, **kwargs)                   ## in order to validate price
        self.maxprice = maxprice
        self.listing = listing

    class Meta:
        model = Bid
        fields = ("price",)
        labels = {"price": '',}
        
        widgets = {
            "price": forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Place Bid'})
        }

    def clean_price(self):
        bid = self.cleaned_data.get('price')      
        if bid is None:
            raise forms.ValidationError('You must enter an amount in order to bid.')
        if self.maxprice is not None:
            if bid <= self.maxprice:
                raise forms.ValidationError('Your bid needs to be higher than current amount')
        else:
            if bid < self.listing.price:
                raise forms.ValidationError("Your bid must be equal or higher than asking price.")
        return bid

class PostComment(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)
        labels = {"comment": '',}
        widgets = {
            "comment": forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Write your comment here...', 'style':'resize:none;'}),
            }


class SelectCategory(ModelForm):
    class Meta:
        model = Listing
        fields = ("category",)
        labels = {"name": "Select Category: ",}
        widgets = {
            "category": forms.SelectMultiple(attrs={'class':'form-control'})
        }