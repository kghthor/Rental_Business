from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'place', 'area', 'bedrooms', 'bathrooms', 'nearby_hospitals', 'nearby_colleges', 'price']
