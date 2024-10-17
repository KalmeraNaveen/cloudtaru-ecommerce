from django.contrib import admin
from .models import ProductsModel,usersmodel
# Register your models here.
class productadmin(admin.ModelAdmin):
    list_display=['id','title','price','category','image','images','description']

class useradmin(admin.ModelAdmin):
    list_display=['id','username','email','password','orders','address','cart']
admin.site.register(ProductsModel,productadmin)
admin.site.register(usersmodel,useradmin)