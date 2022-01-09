from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    Tag,
    ShoppingCart)

EMPTY_VALUE = '-empty-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('color',)
    empty_value_display = EMPTY_VALUE


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
    empty_value_display = EMPTY_VALUE


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'text', 'show_ingredients',
                    'show_tags', 'cooking_time')
    search_fields = ('name', 'description', )
    list_filter = ('author', 'tags')
    empty_value_display = EMPTY_VALUE

    def show_ingredients(self, obj):
        print(obj.__dict__)
        return "\n".join([ingr.name for ingr in obj.ingredients.all()])
    
    def show_tags(self, obj):
        return "\n".join([tag.name for tag in obj.tags.all()])


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = EMPTY_VALUE


class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = EMPTY_VALUE


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingListItemAdmin)