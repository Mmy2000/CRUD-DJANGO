from django.urls import path
from . import views

urlpatterns = [
    path('products/' , views.product_list , name='products'),
    path('products/<int:id>/' , views.product_details , name='product'),
    path('create/' , views.create_product , name='add'),
    path('update/<int:id>/' , views.edite_product , name='update'),
    path('delete/<int:id>/' , views.delete_product , name='delete_product'),
]