from django.http import JsonResponse
from django.shortcuts import render
from .models import Product , ProductImages
from .serializers import ProductSerializer
from rest_framework.decorators import (
    api_view,
)
from .forms import ProductForm , ProductImagesForm
# Create your views here.


@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products , many=True, context={'request':request})
    return JsonResponse({'data':serializer.data})

@api_view(['GET'])
def product_details(request , id):
    product = Product.objects.get(id=id)
    serailizer = ProductSerializer(product, context={'request':request})
    return JsonResponse({'data':serailizer.data})

@api_view(['POST'])
def create_product(request):
    product_form = ProductForm(request.POST , request.FILES)
    if product_form.is_valid():
        product = product_form.save(commit=True)

        product_images = request.FILES.getlist('images')
        for image in product_images:
            product_image_form = ProductImagesForm({'product': product.id}, {'image': image})
            if product_image_form.is_valid():
                product_image = product_image_form.save(commit=False)
                product_image.product = product  # Associate the product with the image
                product_image.save()
            else:
                print("Error with image form:", product_image_form.errors)
                return JsonResponse({'errors': product_image_form.errors}, status=400)
        return JsonResponse({'success':True})
    else:
        print("error",product_form.errors,product_form.non_field_errors)
        return JsonResponse({'errors':product_form.errors.as_json},status=400)

@api_view(["PUT"]) 
def edite_product(request , id):
    try:
        instance_product = Product.objects.get(id=id)
        product_form = ProductForm(
            request.POST , request.FILES , instance=instance_product
        )
        if product_form.is_valid():
            product_form.save()

            if 'images' in request.FILES:
                product_images = request.FILES.getlist('images')
                for image in product_images:
                    product_image_form = ProductImagesForm({'product' : instance_product.id} , {'image' :image})
                    if product_image_form.is_valid():
                        product_image = product_image_form.save(commit=False)
                        product_image.product = instance_product
                        product_image.save()
                    else:
                        print("Error with image form:", product_image_form.errors)
                        return JsonResponse({'errors': product_image_form.errors}, status=400)
                return JsonResponse({"success":True,"message":"Product updated successfully"})
            else:
                return JsonResponse({'error':product_form.errors.as_json()},status = 400)
    
    except Product.DoesNotExist:
        return JsonResponse({"error":"Property not found or you are not authorized to edit it"},status=404)

@api_view(['DELETE']) 
def delete_product(request , id):
    try:
        product = Product.objects.get(id= id)
        product.images.all().delete()
        product.delete()
        return JsonResponse(
                {"success": True, "message": "Property deleted successfully"}
            )
    except Product.DoesNotExist:
        return JsonResponse(
            {"error": "Property not found or you are not authorized to delete it"},
            status=404,
        )