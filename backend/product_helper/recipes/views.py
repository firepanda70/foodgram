import csv

from django.contrib.auth import get_user_model
from django.db.models.aggregates import Sum
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from .models import Tag, Recipe, Ingredient, Favorite, ShoppingCart, IngredientRecipe, MEASURE_CHOICES
from .serializers import TagSerializer, RecipeReadSerializer, IngredientSerializer, RecipeWriteSerializer, ShoppingCartSerializer, FavoriteSerializer, SimpleRecipeSerializer

User = get_user_model()

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = None
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Ingredient.objects.all()

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ('shopping_cart', 'favorite'):
            return SimpleRecipeSerializer
        elif self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipeWriteSerializer
        return RecipeReadSerializer

    @action(methods=['get', 'delete'], detail=False,
            url_path=r'(?P<pk>\d+)/favorite',
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, id=None, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        if request.method == 'GET':
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
    
    @action(methods=['get', 'delete'], detail=False,
            url_path=r'(?P<pk>\d+)/shopping_cart',
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, id=None, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        if request.method == 'GET':
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

    @action(methods=['get'], detail=False,
            url_path='download_shopping_cart',
            url_name='download_shopping_cart',
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request, *args, **kwargs):
        # TODO сделать humanreadable ед измерения 
        response = HttpResponse(content_type='text/csv; charset="UTF-8"')
        response['Content-Disposition'] = ('attachment;'
                                           'filename="Shopping_cart.csv"')
        user = get_object_or_404(User, id=request.user.id)
        recipes = user.shopping_list.values_list('recipe', flat=True)
        queryset = IngredientRecipe.objects.filter(recipe__in=recipes)
        sum_queryset = queryset.values('ingredient__name', 'ingredient__measurement_unit'
                                       ).annotate(Sum('amount'))
        cvv_data = sum_queryset.values_list(
                    'ingredient__name', 'amount__sum', 'ingredient__measurement_unit')
        writer = csv.writer(response)
        writer.writerow(['Ингридиенты', 'Количество', 'ед. изм.'])
        writer.writerows(cvv_data)
        return response