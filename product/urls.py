from django.urls import path
from . import views

urlpatterns = [
    path('products/' , views.product_list , name='product_list'),
    path('products/<int:id>/' , views.product_details , name='product_details'),
    path('create/' , views.create_product , name='create_product'),
    path('update/<int:id>/' , views.edite_product , name='edite_product'),
    path('delete/<int:id>/' , views.delete_product , name='delete_product'),
]