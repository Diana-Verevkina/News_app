from rest_framework import serializers
from news.models import Answer, Comment, News, Profile
import datetime as dt


class NewsSerializer(serializers.ModelSerializer):
    """Сериализер для модели News."""

    class Meta:
        model = News
        fields = ('text', 'author', 'pub_date', 'image')
        read_only_fields = ('author',)


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


class CommentSerializer(serializers.ModelSerializer):
    """Сериализер для модели Comment."""

    class Meta:
        model = Comment
        fields = ('news', 'author', 'text', 'created',)
        read_only_fields = ('author',)


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализер для модели Answer."""

    class Meta:
        model = Answer
        fields = ('id', 'author', 'comment', 'text')
