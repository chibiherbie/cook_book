from django.contrib import admin
from .models import Product, Recipe, RecipeProduct

# Register your models here.
admin.site.register(Product)
admin.site.register(Recipe)
admin.site.register(RecipeProduct)
