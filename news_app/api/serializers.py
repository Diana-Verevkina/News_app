from rest_framework import serializers
from news.models import Comment, News, Profile
import datetime as dt


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
    comments = CommentSerializer(many=True)

    class Meta:
        model = News
        fields = ('text', 'author', 'pub_date', 'image', 'comments')
        read_only_fields = ('author',)
