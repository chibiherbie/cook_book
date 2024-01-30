from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    count_used = models.IntegerField()


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through='RecipeProduct', related_name='recipes')
