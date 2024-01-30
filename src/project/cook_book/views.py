from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .models import Recipe, RecipeProduct, Product


WEIGHT = 10


def add_product_to_recipe(request: HttpRequest, recipe_id: int, product_id: int, weight: int) -> HttpResponse:
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    product = get_object_or_404(Product, pk=product_id)

    recipe_product, created = RecipeProduct.objects.get_or_create(recipe=recipe, product=product)

    recipe_product.weight = weight
    recipe_product.save()

    return HttpResponse(f'Продукт "{product.name}" добавлен в рецепт "{recipe.name}" с весом {weight}гр')


def show_recipes_without_product(request: HttpRequest, product_id: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=product_id)
    recipes_without_product = Recipe.objects.exclude(recipeproduct__product=product) \
                                           .filter(recipeproduct__weight__lt=WEIGHT)

    context = {'product': product, 'recipes': recipes_without_product}
    return render(request, 'recipes_without_product.html', context)


def cook_recipe(request: HttpRequest, recipe_id: int) -> HttpResponse:
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    # Увеличение количества приготовленных блюд для каждого продукта в рецепте
    for recipe_product in recipe.recipeproduct_set.all():
        recipe_product.product.count_used += 1
        recipe_product.product.save()

    return HttpResponse(f'Рецепт "{recipe.name}" приготовлен')
