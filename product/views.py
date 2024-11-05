from django.http import JsonResponse
from .models import Product , ProductImages
from .serializers import ProductSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .forms import ProductForm, ProductImagesForm

# Define parameters for form data
name_param = openapi.Parameter('name', openapi.IN_FORM, description="Name of the product", type=openapi.TYPE_STRING, required=True)
description_param = openapi.Parameter('description', openapi.IN_FORM, description="Description of the product", type=openapi.TYPE_STRING, required=True)
price_param = openapi.Parameter('price', openapi.IN_FORM, description="Price of the product", type=openapi.TYPE_NUMBER, required=True)
image_param = openapi.Parameter('single_image', openapi.IN_FORM, description="Product image", type=openapi.TYPE_FILE, required=True)
images_param = openapi.Parameter(
    'images',
    openapi.IN_FORM,
    description="Product images (select multiple files)",
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_FILE),
    required=True
)

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

@swagger_auto_schema(
    method='post',
    manual_parameters=[name_param, description_param, price_param, image_param,images_param]
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_product(request):
    product_form = ProductForm(request.POST, request.FILES)
    if product_form.is_valid():
        product = product_form.save(commit=True)

        # Process multiple images
        product_images = request.FILES.getlist('images')
        for image in product_images:
            product_image_form = ProductImagesForm({'product': product.id}, {'image': image})
            if product_image_form.is_valid():
                product_image = product_image_form.save(commit=False)
                product_image.product = product  # Associate the product with the image
                product_image.save()
            else:
                return JsonResponse({'errors': product_image_form.errors}, status=400)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'errors': product_form.errors}, status=400)


@swagger_auto_schema(
    method='put',
    manual_parameters=[name_param, description_param, price_param,image_param, images_param]
)
@api_view(["PUT"])
@parser_classes([MultiPartParser, FormParser])
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
    
