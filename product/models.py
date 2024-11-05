from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    single_image = models.ImageField( upload_to='products/single_images', null=True , blank=True)

    def __str__(self):
        return self.name
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product,related_name='images', on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField( upload_to='products/product_images',null=True , blank=True )

    def __str__(self):
        return f'Image for {self.product.name}'
    
    