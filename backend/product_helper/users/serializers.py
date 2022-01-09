from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ParseError

import recipes
from .models import Subscribtion

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        return (not current_user.is_anonymous and Subscribtion.objects.filter(
                user=current_user, author=obj).exists()
                )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password', 'id')
        extra_kwargs = {'email': {'required': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True}, }


"""
class InfoSubscribeSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes_count', 'recipes']

    def get_recipes_count(self, obj):
        return obj.user_recipes.count()

    def get_recipes(self, obj):
        obj = obj.user_recipes.all()
        params = self.context['request'].query_params
        limit = params.get('recipes_limit')
        if limit:
            obj = obj[:int(limit)]      
        return recipes.serializers.SimpleRecipeSerializer(obj, many=True).data


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = '__all__'

    def validate(self, attrs):
        author = attrs.get('subscription')
        user = self.context.get('request').user
        if user == author:
            raise ParseError(detail='Нельзя подписаться на самого себя.')
        return attrs

    def to_representation(self, obj):
        return InfoSubscribeSerializer(
            obj.subscription, context=self.context).data
"""
