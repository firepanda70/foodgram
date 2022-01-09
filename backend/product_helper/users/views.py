from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .models import Subscribtion
from .serializers import CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.all()

    def get_instance(self):
        return self.request.user

"""
class SubscribeViewSet(ModelViewSet):
    http_method_names = ['get', 'delete', ]
    serializer_class = SubscribeSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Subscribtion.objects.all()
    lookup_url_kwarg = 'id'
    lookup_field = 'subscription'

    def create(self, request, *args, **kwargs):
        subscription = get_object_or_404(User, id=self.kwargs['id'])
        user = request.user.id
        data = {'subscription': subscription.id,
                'user': user}
        request.data.update(data)
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.subscriptions.all()

    @action(['get', 'delete'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.create(request, *args, **kwargs)
        else:
            return self.destroy(request, *args, **kwargs)
"""