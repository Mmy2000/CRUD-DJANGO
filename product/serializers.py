from rest_framework import serializers

from product.models import Product , ProductImages


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductImages
        fields = ['id','image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True) 
    class Meta:
        model=Product
        fields = ['id','name' , 'price' , 'description' , 'single_image' , 'images']