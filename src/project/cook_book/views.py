from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .models import Recipe, RecipeProduct, Product


FILTER_MIN_WEIGHT = 10


def add_product_to_recipe(request: HttpRequest, recipe_id: int, product_id: int, weight: int) -> HttpResponse:
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    product = get_object_or_404(Product, pk=product_id)

    # Проверка, что продукт с таким ID не включен в рецепт
    if recipe.recipeproduct_set.filter(product=product).exists():
        return HttpResponse(f'Продукт "{product.name}" уже есть в рецепте')

    recipe_product, created = RecipeProduct.objects.get_or_create(recipe=recipe, product=product)

    recipe_product.weight = weight
    recipe_product.save()

    return HttpResponse(f'Продукт "{product.name}" добавлен в рецепт "{recipe.name}" с весом {weight}гр')


def show_recipes_without_product(request: HttpRequest, product_id: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=product_id)

    recipes_without_product = Recipe.objects.exclude(recipeproduct__product=product)
    recipes_with_low_quantity = Recipe.objects.filter(recipeproduct__product=product,
                                                      recipeproduct__weight__lt=MIN_WEIGHT)

    recipes = recipes_without_product.union(recipes_with_low_quantity)

    context = {'product': product, 'recipes': recipes}
    return render(request, 'recipes_without_product.html', context)


def cook_recipe(request: HttpRequest, recipe_id: int) -> HttpResponse:
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    # Увеличение количества приготовленных блюд для каждого продукта в рецепте
    for recipe_product in recipe.recipeproduct_set.all():
        recipe_product.product.count_used += 1
        recipe_product.product.save()

    return HttpResponse(f'Рецепт "{recipe.name}" приготовлен')
