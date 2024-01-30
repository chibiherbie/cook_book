from django.contrib import admin
from .models import Product, Recipe, RecipeProduct
from django import forms


class RecipeProductInlineForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        if self.instance.pk is None and product.recipeproduct_set.filter(recipe=self.cleaned_data['recipe']).exists():
            raise forms.ValidationError('Этот продукт уже есть в рецепте')
        return cleaned_data


class RecipeProductInline(admin.TabularInline):
    model = RecipeProduct
    form = RecipeProductInlineForm
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeProductInline]


admin.site.register(Product)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeProduct)
