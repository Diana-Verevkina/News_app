from rest_framework import serializers
from news.models import News


class NewsSerializer(serializers.ModelSerializer):
    """Сериализер для модели News."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = News
        fields = '__all__'