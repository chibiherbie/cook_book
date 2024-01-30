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


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product_1 = Product.objects.create(name='Помидоры')
        self.product_2 = Product.objects.create(name='Огурцы')
        self.recipe = Recipe.objects.create(name='Салат')
        self.recipe_product = RecipeProduct.objects.create(recipe=self.recipe, product=self.product_1, weight=100)

    def test_add_product_to_recipe(self):
        url = reverse('add_product_to_recipe', args=[self.recipe.id, self.product_2.id, 20])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Продукт "{self.product_2.name}" добавлен')
        self.assertEqual(self.recipe.products.count(), 2)

    def cook_recipe(self):
        url = reverse('cook_recipe', args=[self.recipe.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product_1.count_used, 1)

    def test_show_recipes_without_product(self):
        url = reverse('show_recipes_without_product', args=[self.product_2.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Салат')

    def test_show_recipes_min_weight(self):
        # Добавляем продукт с весом меньше 10г
        url_add_product = reverse('add_product_to_recipe', args=[self.recipe.id, self.product_2.id, 5])
        self.client.get(url_add_product)

        url = reverse('show_recipes_without_product', args=[self.product_2.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.recipe.products.count(), 2)
        self.assertContains(response, 'Салат')
