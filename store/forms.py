from django import forms
from .models import Profile, Item

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location']  

class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'stock', 'description', 'image']