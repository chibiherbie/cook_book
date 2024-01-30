from django.test import TestCase, Client
from .models import Product, Recipe, RecipeProduct
from django.urls import reverse


class ModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Помидоры')
        self.recipe = Recipe.objects.create(name='Салат')

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Помидоры')

    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), 'Салат')

    def test_add_product_to_recipe(self):
        recipe_product = RecipeProduct.objects.create(recipe=self.recipe, product=self.product, weight=100)
        self.assertEqual(recipe_product.recipe, self.recipe)
        self.assertEqual(recipe_product.product, self.product)
        self.assertEqual(recipe_product.weight, 100)
