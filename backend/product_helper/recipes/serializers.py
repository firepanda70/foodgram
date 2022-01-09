from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, relations
from rest_framework.exceptions import ValidationError

from users.serializers import CustomUserSerializer
from .models import Favorite, Tag, Recipe, Ingredient, IngredientRecipe, ShoppingCart, MEASURE_CHOICES


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.ChoiceField(choices=MEASURE_CHOICES)

    class Meta:
        model = Ingredient
        fields = '__all__'

    def to_representation(self, value):
        res = super().to_representation(value)
        res['measurement_unit'] = value.get_measurement_unit_display()
        return res

class IngredientAmountReadSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id',
        queryset=Ingredient.objects.all()
    )
    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')

    def to_representation(self, value):
        res = super().to_representation(value)
        res['measurement_unit'] = value.ingredient.get_measurement_unit_display()
        return res


class IngredientAmountWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        read_only=True,
        many=True
    )
    author = CustomUserSerializer(
        read_only=True
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True,
        required=False
    )
    ingredients = IngredientAmountReadSerializer(
        read_only=True,
        many=True,
        source='related_ingredient'
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name', 
            'cooking_time',
            'author', 
            'ingredients',
            'tags',
            'image',
            'text',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.shopping_list.filter(recipe=obj).exists()


class SimpleRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None,
        use_url=True,
        required=False
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True,
        required=False
    )
    ingredients = IngredientAmountWriteSerializer(
        many=True,
        source='related_ingredient',
        required=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        author = self.context['request'].user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('related_ingredient')
        recipe = Recipe.objects.create(**validated_data, author=author)
        self.add_tags_and_ingredients(tags, ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image', instance.image)
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('related_ingredient')
        self.add_tags_and_ingredients(tags, ingredients, instance)
        super().update(instance, validated_data)
        return instance

    def add_tags_and_ingredients(self, tags, ingredients, recipe):
        recipe.tags.set(tags)
        IngredientRecipe.objects.filter(recipe=recipe).delete()
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['id']
            )

    def to_representation(self, instanse):
        return RecipeReadSerializer(
            instanse,
            context={'request': self.context.get('request')}
        ).data

class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('user', 'recipe')
        model = Favorite
