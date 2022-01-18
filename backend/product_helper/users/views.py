from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Subscribtion
from .serializers import (CustomUserCreateSerializer, CustomUserSerializer,
                          SubscribeSerializer, UserSubscriptionSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ('subscriptions', 'subscribe'):
            return UserSubscriptionSerializer
        elif self.action == 'subscribe':
            return SubscribeSerializer
        elif self.action == 'create':
            return CustomUserCreateSerializer
        return CustomUserSerializer

    def get_permissions(self):
        # По сравнению с методом в родительским классе,
        # изменение только с list и retrieve
        permissions = settings.PERMISSIONS
        if self.action in ('retrieve', 'list'):
            self.permission_classes = (permissions.AllowAny,)
        if self.action == 'create':
            self.permission_classes = permissions.user_create
        elif self.action == 'activation':
            self.permission_classes = permissions.activation
        elif self.action == 'resend_activation':
            self.permission_classes = permissions.password_reset
        elif self.action == 'reset_password':
            self.permission_classes = permissions.password_reset
        elif self.action == 'reset_password_confirm':
            self.permission_classes = permissions.password_reset_confirm
        elif self.action == 'set_password':
            self.permission_classes = permissions.set_password
        elif self.action == 'set_username':
            self.permission_classes = permissions.set_username
        elif self.action == 'reset_username':
            self.permission_classes = permissions.username_reset
        elif self.action == 'reset_username_confirm':
            self.permission_classes = permissions.username_reset_confirm
        elif self.action == 'destroy' or (
            self.action == 'me' and
            self.request and
            self.request.method == 'DELETE'
        ):
            self.permission_classes = settings.PERMISSIONS.user_delete
        return [permission() for permission in self.permission_classes]

    def get_instance(self):
        return self.request.user

    @action(methods=('get',), detail=False,
            url_path='subscriptions',
            permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request, *args, **kwargs):
        # TODO: наверняка можно по-красивее сделать
        subscriptions = User.objects.filter(followers__user=request.user).all()
        page = self.paginate_queryset(subscriptions)
        serializer = self.get_serializer_class()(
            subscriptions,
            context={'request': request},
            many=True
        )
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=('post', 'delete'), detail=False,
            url_path=r'(?P<id>\d+)/subscribe',
            permission_classes=(permissions.IsAuthenticated,))
    def subscribe(self, request, *args, **kwargs):
        # TODO: наверняка можно по-красивее сделать
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        if request.method == 'POST':
            data = {
                'author': author.id,
                'user': request.user.id
            }
            request.data.update(data)
            serializer = SubscribeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.retrieve(request)

        subscription = get_object_or_404(
            Subscribtion,
            user=request.user,
            author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
