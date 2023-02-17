import pytest


@pytest.fixture
def news(user):
    from news_app.news.models import News
    return News.objects.create(text='Тестовый пост 1', author=user,)

"""
@pytest.fixture
def post_2(user):
    from news.models import News
    return News.objects.create(text='Тестовый пост 12342341', author=user,)


@pytest.fixture
def another_post(another_user):
    from news.models import News
    return News.objects.create(text='Тестовый пост 2', author=another_user,)
"""