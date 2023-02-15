from django.shortcuts import get_object_or_404
from news.models import News, Profile
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated

from .permissions import IsAuthorOrReadOnly
from .mixins import LikedMixin
from .serializers import CommentSerializer, FollowSerializer, \
    NewsSerializer, ProfileSerializer


class NewsViewSet(LikedMixin, viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = PageNumberPagination
    ordering_fields = ['pub_date']
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = None

    def get_news(self):
        return get_object_or_404(News, id=self.kwargs.get('news_id'))

    def get_queryset(self):
        return self.get_news().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, news=self.get_news())


class FollowViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                    mixins.ListModelMixin):
    serializer_class = FollowSerializer
    search_fields = ('user__username', 'author__username')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
