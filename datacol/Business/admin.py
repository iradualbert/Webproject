from django.contrib import admin
from .models import Product, ProductQuestion, ProductAnswer, Picture
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductQuestion)
admin.site.register(ProductAnswer)
admin.site.register(Picture)