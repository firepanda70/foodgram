from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from .models import Subscribtion

User = get_user_model()


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


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        return (not current_user.is_anonymous and
                current_user.subsctiptions.filter(
                    author=obj).exists())


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password', 'id')
        extra_kwargs = {'email': {'required': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True}, }


class UserSubscriptionSerializer(CustomUserSerializer):
    recipes = SimpleRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes_count', 'recipes')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        params = self.context['request'].query_params
        limit = params.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        return SimpleRecipeSerializer(obj, many=True).data


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribtion
        fields = '__all__'

    def validate(self, attrs):
        author = attrs.get('author')
        user = attrs.get('user')
        if user == author:
            raise ParseError(detail='Нельзя подписаться на самого себя.')
        return attrs

    def to_representation(self, obj):
        return UserSubscriptionSerializer(
            obj.subscription, context=self.context).data
