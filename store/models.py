from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BrandModel(models.Model):
    brand=models.CharField(max_length=100)
    # image=models.ImageField(upload_to='brandimage', default=None)

    def __str__(self):
        return str(self.brand)
    
class CategoryModel(models.Model):
    category=models.CharField(max_length=100)
    def __str__(self):
        return str(self.category)

class ProductModel(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=50)
    discount_percent=models.IntegerField(default=None)
    selling_price=models.FloatField(max_length=50)
    discounted_price=models.FloatField(max_length=50)
    p_brand=models.ForeignKey(BrandModel, on_delete=models.CASCADE)
    p_category=models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    featured=models.BooleanField(default=False)
    image=models.ImageField(upload_to='productimage')
    def __str__(self):
        return str(self.id)
    
class ProductImageModel(models.Model):
    productid = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    productimage = models.ImageField(upload_to='productimg')
    
class ProductDescriptionModel(models.Model):
    productid = models.ForeignKey(ProductModel, on_delete = models.CASCADE)
    title = models.CharField(max_length=100, default=None)
    titledescription = models.CharField(max_length=500, default=None)
    titleimage=models.ImageField(upload_to='descriptionimg')
    touch = models.CharField(max_length=100, default=None)
    touchdescription = models.CharField(max_length=500, default=None)
    touchimage=models.ImageField(upload_to='descriptionimg')
    camera = models.CharField(max_length=100, default=None)
    cameradescription = models.CharField(max_length=500, default=None)
    cameraimage=models.ImageField(upload_to='descriptionimg')
    technology = models.CharField(max_length = 100, default = None)
    technologydescription = models.CharField(max_length=500, default=None)
    technologyimage=models.ImageField(upload_to='descriptionimg')
    design = models.CharField(max_length=100, default=None)
    designdescription = models.CharField(max_length=500, default=None)
    designimage=models.ImageField(upload_to='descriptionimg')
    

class CustomerModel(models.Model):
    username = models.ForeignKey(User, on_delete = models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100, default=None)
    areacode = models.IntegerField(default = None)
    phone = models.IntegerField(default = None)
    address = models.CharField(max_length=100)
    zipcode =  models.IntegerField(default = None)

class ProductShortDescriptionModel(models.Model):
    productname = models.ForeignKey(ProductModel, on_delete = models.CASCADE)
    description = models.TextField(default=None)
    

class AdditionalInformationModel(models.Model):
    productname = models.ForeignKey(ProductModel, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()



class ReviewModel(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    titleproduct = models.ForeignKey(ProductModel,on_delete = models.CASCADE)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    review = models.TextField()
    rating = models.IntegerField()
    date = models.DateTimeField( auto_now_add = True)


class CartModel(models.Model):
    productid= models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    username= models.ForeignKey(User, on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField(default=1)
    def total_product_price(self):
        return int((self.quantity*self.productid.discounted_price))