from rest_framework import serializers
from news.models import Comment, News, Profile
import datetime as dt
from news import services as likes_services
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализер для модели Profile."""

    class Meta:
        model = Profile
        fields = ('user', 'first_name', 'last_name', 'birth_year',
                  'description', 'image')
        read_only_fields = ('user',)

    def validate_birth_year(self, value):
        year = dt.date.today().year
        if not (year - 120 < value <= year):
            raise serializers.ValidationError('Проверьте год рождения!')
        return value


class FilterCommentListSerializer(serializers.ListSerializer):
    """Фильтр комментариев. Только Parents."""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализер для модели Comment."""

    children = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        list_serializer_class = FilterCommentListSerializer
        fields = ('id', 'news', 'author', 'text', 'created', 'parent',
                  'children')
        read_only_fields = ('author',)


class NewsSerializer(serializers.ModelSerializer):
    """Сериализер для модели News."""
    comments = CommentSerializer(many=True, required=False)
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ('id','text', 'author', 'pub_date', 'image', 'comments', 'is_fan',
                  'total_likes')
        read_only_fields = ('author',)

    def get_is_fan(self, obj) -> bool:
        """Проверяет, лайкнул ли `request.user` новость (`obj`)."""
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)


class FanSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'full_name',
        )

    def get_full_name(self, obj):
        return obj.get_full_name()
