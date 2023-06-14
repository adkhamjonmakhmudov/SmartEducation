from django.shortcuts import render
from django.utils import translation
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from courses.permissions import ManagerandDirectorOrReadOnly

from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.authtoken.models import Token
from rest_framework import generics, status


def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response
# ####################
# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .serializer import *
from .models import *
from rest_framework import status
from rest_framework.response import Response
# Director Table
class DirectorViewset(ModelViewSet):
    queryset =  Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [ManagerandDirectorOrReadOnly]
    def create(self, request, *args, **kwargs):
        data =  request.data
        try:
            director = Director.objects.create_user(username=data['username'],password=data['password'])
            serializer = DirectorSerializer(director,partial=True)
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        except:
            return Response({'error':'Please be aware'})
    def update(self, request, *args, **kwargs):
        director  =  self.get_object()
        data = request.data
        director.username = data.get('username',director.username)
        director.password = data.get('password',director.password)
        director.save()
        serializer = DirectorSerializer(director,partial=True)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
# Manager Table
class ManagerViewset(ModelViewSet):
    queryset =  Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = ManagerandDirectorOrReadOnly
    def create(self, request, *args, **kwargs):
        data =  request.data
        try:
            manager = Manager.objects.create_user(username=data['username'],password=data['password'])
            serializer = ManagerSerializer(manager,partial=True)
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        except:
            return Response({'error':'Please be aware'})
    def update(self, request, *args, **kwargs):
        manager  =  self.get_object()
        data = request.data
        manager.username = data.get('username',manager.username)
        manager.password = data.get('password',manager.password)
        manager.save()
        serializer = ManagerSerializer(manager,partial=True)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class LoginAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)