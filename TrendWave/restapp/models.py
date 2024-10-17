from django.db import models

# Create your models here.
class ProductsModel(models.Model):
    title=models.CharField(max_length=255)
    price=models.FloatField()
    category=models.CharField(max_length=345,default="")
    image=models.URLField()
    images=models.TextField()
    description=models.TextField()

class usersmodel(models.Model):
    username=models.CharField(max_length=355)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    address=models.TextField(default='null')
    orders=models.TextField(default='null')
    cart = models.TextField(blank=True, default='')
