import os

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag, User)
from .permissions import AuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer,
                          ShoppingCartSerializer, SimpleRecipeSerializer,
                          TagSerializer)


FILENAME = 'Shopping_cart.txt'
FILETYPE = 'text/plain; charset="UTF-8"'


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = None
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = None
    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (AuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('shopping_cart', 'favorite'):
            return SimpleRecipeSerializer
        elif self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipeWriteSerializer
        return RecipeReadSerializer

    @action(methods=('post', 'delete'), detail=False,
            url_path=r'(?P<pk>\d+)/favorite',
            permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        if request.method == 'POST':
            favorite_serializer = FavoriteSerializer(
                data={'user': user.id, 'recipe': recipe.id}
            )
            favorite_serializer.is_valid(raise_exception=True)
            favorite_serializer.save()
            return self.retrieve(request)
        elif request.method == 'DELETE':
            favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('post', 'delete'), detail=False,
            url_path=r'(?P<pk>\d+)/shopping_cart',
            permission_classes=(permissions.IsAuthenticated,))
    def shopping_cart(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        if request.method == 'POST':
            shop_serializer = ShoppingCartSerializer(
                data={'user': user.id, 'recipe': recipe.id}
            )
            shop_serializer.is_valid(raise_exception=True)
            shop_serializer.save()
            return self.retrieve(request)
        elif request.method == 'DELETE':
            cart = get_object_or_404(ShoppingCart, user=user, recipe=recipe)
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('get',), detail=False,
            url_path='download_shopping_cart',
            url_name='download_shopping_cart',
            permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request, *args, **kwargs):
        # TODO сделать pdf
        user = get_object_or_404(User, id=request.user.id)
        recipes = user.shopping_list.values_list('recipe', flat=True)
        queryset = IngredientRecipe.objects.filter(recipe__in=recipes).all()
        result = {}
        for ing_res in queryset:
            ing = ing_res.ingredient
            if ing.name not in result.keys():
                result[ing.name] = {
                    'name': ing.name,
                    'amount': ing_res.amount,
                    'unit': ing.get_measurement_unit_display()
                }
            else:
                result[ing.name]['amount'] += ing_res.amount

        lines = ['Ингридиенты, Количество, ед. изм.\n']
        for line in result.values():
            lines.append('{name}, {amount}, {unit}\n'.format(**line))

        with open(FILENAME, 'x') as shopping_list:
            shopping_list.writelines(lines)
        with open(FILENAME, 'r') as shopping_list:
            response = HttpResponse(shopping_list, content_type=FILETYPE)
            response['Content-Disposition'] = ('attachment;'
                                               f'filename="{FILENAME}"')
        os.remove(os.path.abspath(FILENAME))
        return response
