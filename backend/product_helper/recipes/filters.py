import urllib

from django_filters import rest_framework as filters

from .models import Ingredient, Recipe, Tag, User


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='slug',
        queryset=Tag.objects.all()
    )
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='favorite_filter')
    is_in_shopping_cart = filters.BooleanFilter(method='shopping_card_filter')

    def favorite_filter(self, queryset, name, value):
        if value == 1:
            return queryset.filter(users_favorites__user=self.request.user)
        return queryset

    def shopping_card_filter(self, queryset, name, value):
        if value == 1:
            return queryset.filter(users_carts__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author')


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(method='name_filter')

    def name_filter(self, queryset, name, value):
        decoded_value = urllib.parse.unquote_plus(value)
        return queryset.filter(name__icontains=decoded_value)

    class Meta:
        model = Ingredient
        fields = ('name',)
