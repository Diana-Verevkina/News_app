import os

import pytest
from django.contrib.auth import get_user_model
from django.core import mail

User = get_user_model()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_app.settings')

from news_app.news.models import Category


def test_create_category(db):
    category = Category.objects.create(name="Books")
    assert category.name == "Books"