from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import (TagViewSet, RecipeViewSet, IngredientViewSet)
from users.views import CustomUserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet)
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='resipes')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
# router_v1.register('users', SubscribeViewSet)

# from users.views

app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    # path('users/subscriptions/', SubscribeViewSet, ),
    path('', include(router_v1.urls)),
]