from django import forms
from .models import *

class ListingForm(forms.ModelForm):
    seller_name = forms.CharField(max_length=10, required = True)
    book_image = forms.ImageField()
    book_title = forms.CharField(max_length=100, required=True)
    author = forms.CharField(max_length=50, required=True)
    isbn = forms.CharField(max_length=20, required=True)
    book_course = forms.CharField(max_length=20)
    price = forms.DecimalField(max_digits=4, decimal_places=2, required=True) 
    book_description = forms.CharField(max_length=500)

    class Meta:
        model = Listing
        fields = ('seller_name','book_image','book_title','author','isbn','book_course','price', 'book_description')