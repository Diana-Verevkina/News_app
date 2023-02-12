from django.shortcuts import get_object_or_404
from news.models import News, Profile, User
from rest_framework import viewsets

from .mixins import LikedMixin
from .serializers import CommentSerializer, NewsSerializer, ProfileSerializer


class NewsViewSet(LikedMixin, viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    # serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_news(self):
        return get_object_or_404(News, id=self.kwargs.get('news_id'))

    def get_queryset(self):
        return self.get_news().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, news=self.get_news())
