from datetime import datetime

from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework.exceptions import NotFound
from rest_framework.generics import (
    CreateAPIView, UpdateAPIView, RetrieveAPIView, RetrieveUpdateAPIView,
    DestroyAPIView
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
)

from . import serializers
from .models import UserPref, Dog, UserDog
from .permissions import IsOwnerOrReadOnly
from .serializers import DogSerializer, UserPrefSerializer


class UserRegisterView(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class CreateDogView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = DogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(added_by=self.request.user)
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class DeleteDogView(DestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Dog.objects.all()


class StatusView(RetrieveAPIView):
    serializer_class = DogSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance:
            serializer = self.get_serializer(instance)
            can_delete = request.user.is_staff or request.user == instance.added_by
            first = instance.first
            data = {'can_delete': can_delete, 'first': first}
            data.update(serializer.data)

            return Response(data=data)
        else:
            raise NotFound(detail='Last Entry')

    def get_queryset(self, pk=None):
        status = self.kwargs.get('status')[0]  # First letter of status.
        user = self.request.user

        if hasattr(user, 'userpref'):  # Superusers may have no userpref.
            dogs = user.userpref.get_preferred_dogs()
        else:
            dogs = Dog.objects.all()

        if status in 'ld':  # Liked/Disliked: return dogs linked to UserDog for user.
            return dogs.filter(userdog__user=user, userdog__status=status).exclude(userdog__hidden=True)

        else:  # Undecided: return dogs not linked to UserDog object for user.
            return dogs.exclude(userdog__user=user)

    def get_object(self, prev=False):
        dogs = self.get_queryset()

        if dogs:
            pk = self.kwargs.get('pk')

            if prev:
                dog = dogs.filter(pk__lt=pk).last()
                if not dog:
                    dog = dogs.first()
            else:
                dog = dogs.filter(pk__gt=pk).first()

            if dog:
                dog.first = True if dog == dogs.first() else False  # first dog

            return dog
        else:
            raise NotFound(detail='No Results')


class NextStatusView(StatusView):
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PrevStatusView(StatusView):
    def get_object(self, prev=True):
        return super().get_object(prev)


class SetStatusView(UpdateAPIView):
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        status = kwargs.get('status')[0]  # Get first letter of status.
        user = self.request.user
        dog = Dog.objects.get(pk=pk)
        userdog, _ = UserDog.objects.get_or_create(user=user, dog=dog)

        if status in 'ld':
            userdog.status = status
            userdog.save()
            print('SAVED AT:', datetime.now())
        else:
            userdog.delete()

        return Response(data={'pk': pk}, status=HTTP_200_OK)


class HideDogView(UpdateAPIView):
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = self.request.user
        dog = Dog.objects.get(pk=pk)
        userdog, _ = UserDog.objects.get_or_create(user=user, dog=dog)

        userdog.hidden = True
        userdog.save()

        return Response(data={'pk': pk}, status=HTTP_200_OK)


class SetPrefView(RetrieveUpdateAPIView):
    queryset = UserPref.objects.all()
    serializer_class = UserPrefSerializer

    def get_object(self):
        userpref, _ = UserPref.objects.get_or_create(user=self.request.user)
        return userpref
