import pytest


@pytest.fixture
def news(user):
    from news.models import News
    return News.objects.create(text='Тестовый пост 1', author=user,)


@pytest.fixture
def news_2(user):
    from news.models import News
    return News.objects.create(text='Тестовый пост 2', author=user,)


@pytest.fixture
def another_news(another_user):
    from news.models import News
    return News.objects.create(text='Тестовый пост 3', author=another_user,)


@pytest.fixture
def comment_1_news(news, user):
    from news.models import Comment
    return Comment.objects.create(author=user, news=news, text='Коммент 1')


@pytest.fixture
def comment_2_news(news, another_user):
    from news.models import Comment
    return Comment.objects.create(author=another_user, news=news,
                                  text='Коммент 2')


@pytest.fixture
def comment_1_another_news(another_news, user):
    from news.models import Comment
    return Comment.objects.create(author=user, news=another_news,
                                  text='Коммент 12')


@pytest.fixture
def follow_1(user, another_user):
    from news.models import Follow
    return Follow.objects.create(user=user, author=another_user)


@pytest.fixture
def follow_2(user_2, user):
    from news.models import Follow
    return Follow.objects.create(user=user_2, author=user)


@pytest.fixture
def follow_3(user_2, another_user):
    from news.models import Follow
    return Follow.objects.create(user=user_2, author=another_user)


@pytest.fixture
def follow_4(another_user, user):
    from news.models import Follow
    return Follow.objects.create(user=another_user, author=user)


@pytest.fixture
def follow_5(user_2, user):
    from news.models import Follow
    return Follow.objects.create(user=user, author=user_2)

