import datetime as dt

from django.contrib.auth import get_user_model
from news import services as likes_services
from news.models import Comment, Follow, News, Profile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


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
    created = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        list_serializer_class = FilterCommentListSerializer
        fields = ('id', 'news', 'author', 'text', 'created',
                  'parent', 'children')
        read_only_fields = ('author', 'created')


class NewsSerializer(serializers.ModelSerializer):
    """Сериализер для модели News."""
    comments = CommentSerializer(many=True, required=False)
    is_fan = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    pub_date = serializers.DateTimeField(format="%Y-%m-%d", required=False)

    class Meta:
        model = News
        fields = ('id', 'text', 'author', 'pub_date', 'image', 'comments',
                  'is_fan', 'total_likes')
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


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализер для модели Profile."""
    user = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    age = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'user', 'first_name', 'last_name', 'birth_year', 'age',
                  'description', 'image',)
        read_only_fields = ('user',)

    def validate_birth_year(self, value):
        year = dt.date.today().year
        if not (year - 120 < value <= year):
            raise serializers.ValidationError('Проверьте год рождения!')
        return value

    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    author = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=['user', 'author'])]

    def validate_author(self, data):
        if self.context['request'].user != data:
            return data
        raise serializers.ValidationError('Нельзя подписаться на себя')
