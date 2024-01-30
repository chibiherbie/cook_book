from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Recipe, RecipeProduct, Product


def add_product_to_recipe(recipe_id, product_id, weight):
    recipe = Recipe.objects.get(id=recipe_id)
    product = Product.objects.get(id=product_id)
    try:
        recipe_product = RecipeProduct.objects.get(recipe=recipe, product=product)
        recipe_product.weight = weight
        recipe_product.save()
    except RecipeProduct.DoesNotExist:
        recipe.products.add(product, through_defaults={'weight': weight})


def show_recipes_without_product(request, product_id=1):
    recipes_without_product = Recipe.objects.exclude(recipeproduct__product_id=product_id).distinct()
    recipes_with_low_quantity = Recipe.objects.filter(recipeproduct__product_id=product_id,
                                                      recipeproduct__weight__lt=10).distinct()

    template = loader.get_template('recipes_without_product.html')
    context = {
        'recipes_without_product': recipes_without_product,
        'recipes_with_low_quantity': recipes_with_low_quantity,
    }

    return HttpResponse(template.render(context, request))


def cook_recipe(recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    recipe_products = recipe.products.all()
    for recipe_product in recipe_products:
        product = recipe_product.product
        product.times_used += 1
        product.save()
