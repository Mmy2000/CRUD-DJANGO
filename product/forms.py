from django.forms import ModelForm
from .models import Product , ProductImages
from django import forms

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'price',
            'description',
            'single_image',
        )

class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ("image",)