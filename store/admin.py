from django.contrib import admin

# Register your models here.
from .models import (ProductModel, BrandModel, CategoryModel, ProductDescriptionModel, 
                     ProductShortDescriptionModel, AdditionalInformationModel, ProductImageModel, ReviewModel, CartModel, CustomerModel
                            )

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=[
        'title', 'description', 'selling_price', 'discounted_price', 'image'
    ]

    
@admin.register(BrandModel)
class BrandModelAdmin(admin.ModelAdmin):
    list_display=[
        'brand'
    ]

    
@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display=[
        'category'
    ]

@admin.register(ProductDescriptionModel)
class ProductDescriptionModelAdmin(admin.ModelAdmin):
    list_display = ['productid', 'title', 'titledescription', 'titleimage', 
                    'touch', 'touchdescription', 'touchimage',
                    'camera', 'cameradescription', 'cameraimage',
                    'technology', 'technologydescription', 'technologyimage',
                    'design', 'designdescription', 'designimage']

@admin.register(ProductShortDescriptionModel)
class ProductShortDescriptionModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'productname', 'description']

@admin.register(AdditionalInformationModel)
class AdditionalInformationModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'productname', 'title', 'description']

@admin.register(ProductImageModel)
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display= ['productid', 'productimage']

@admin.register(CartModel)
class CartModelAdmin(admin.ModelAdmin):
    list_display=[
        'productid', 'username', 'quantity']
    

@admin.register(CustomerModel)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=[
        'username', 'fname', 'lname', 'areacode', 'phone','address', 'zipcode' ]
    

@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display= []