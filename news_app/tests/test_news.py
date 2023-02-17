import pytest
from news.models import News


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='TestUser',
                                                 password='vfghnj1234567')


@pytest.fixture
def user_2(django_user_model):
    return django_user_model.objects.create_user(username='TestUser2',
                                                 password='1hurdyrtgj234567')


@pytest.fixture
def another_user(django_user_model):
    return django_user_model.objects.create_user(username='TestUserAnother',
                                                 password='iuytfbnjkmnbg646')


@pytest.fixture
def token(user):
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@pytest.fixture
def user_client(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token["access"]}')
    return client


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


class TestPostAPI:

    @pytest.mark.django_db(transaction=True)
    def test_news_page_not_found(self, client, news):
        response = client.get('/v1/news/')

        assert response.status_code != 404, (
            'Страница `/v1/news/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_news_list_not_auth(self, client, news):
        response = client.get('/v1/news/')

        assert response.status_code == 200, (
            'Проверьте, что на `/v1/news/` при запросе без токена возвращаете '
            'статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_news_single_not_auth(self, client, news):
        response = client.get(f'/v1/news/{news.id}/')

        assert response.status_code == 200, (
            'Проверьте, что на `/v1/news/{news.id}/` при запросе без токена '
            'возвращаете статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_posts_auth(self, user_client, news, another_news):
        response = user_client.get('/v1/news/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/v1/news/` с токеном авторизации '
            'возвращается статус 200'
        )

        test_data = response.json()

        # response without pagination must be a list type
        assert type(test_data) == list, (
            'Проверьте, что при GET запросе на `/v1/news/` без пагинации, '
            'возвращается список'
        )

        assert len(test_data) == News.objects.count(), (
            'Проверьте, что при GET запросе на `/v1/news/` без пагинации '
            'возвращается весь список статей'
        )

        news = News.objects.all()[0]
        test_news = test_data[0]
        assert 'id' in test_news, (
            'Проверьте, что добавили `id` в список полей `fields` '
            'сериализатора модели News'
        )
        assert 'text' in test_news, (
            'Проверьте, что добавили `text` в список полей `fields` '
            'сериализатора модели News'
        )
        assert 'author' in test_news, (
            'Проверьте, что добавили `author` в список полей `fields` '
            'сериализатора модели News'
        )
        assert 'pub_date' in test_news, (
            'Проверьте, что добавили `pub_date` в список полей `fields` '
            'сериализатора модели News'
        )
        assert test_news['author'] == news.author.username, (
            'Проверьте, что `author` сериализатора модели Post возвращает '
            'имя пользователя'
        )

        assert test_news['id'] == news.id, (
            'Проверьте, что при GET запросе на `/v1/news/` возвращается весь '
            'список статей'
        )

    @pytest.mark.django_db(transaction=True)
    def test_news_get_paginated(self, user_client, news, news_2, another_news):
        base_url = '/v1/news/'
        limit = 2
        offset = 2
        url = f'{base_url}?limit={limit}&offset={offset}'
        response = user_client.get(url)
        assert response.status_code == 200, (
            f'Проверьте, что при GET запросе `{url}` с токеном авторизации '
            f'возвращается статус 200'
        )

        test_data = response.json()

        # response with pagination must be a dict type
        assert type(test_data) == dict, (
            f'Проверьте, что при GET запросе на `{url}` с пагинацией, '
            f'возвращается словарь'
        )
        assert "results" in test_data.keys(), (
            f'Убедитесь, что при GET запросе на `{url}` с пагинацией, ключ '
            f'`results` присутствует в ответе'
        )
        assert len(test_data.get('results')) == News.objects.count() - offset, (
            f'Проверьте, что при GET запросе на `{url}` с пагинацией, '
            f'возвращается корректное количество статей'
        )
        assert test_data.get('results')[0].get('text') == another_news.text, (
            f'Убедитесь, что при GET запросе на `{url}` с пагинацией, '
            'в ответе содержатся корректные статьи'
        )

        news = News.objects.get(text=another_news.text)
        test_news = test_data.get('results')[0]
        assert 'id' in test_news, (
            'Проверьте, что добавили `id` в список полей `fields` '
            'сериализатора модели News'
        )
        assert 'text' in test_news, (
            'Проверьте, что добавили `text` в список полей `fields` '
            'сериализатора модели News'
        )
        assert 'author' in test_news, (
            'Проверьте, что добавили `author` в список полей `fields` '
            'сериализатора модели News'
        )
        assert 'pub_date' in test_news, (
            'Проверьте, что добавили `pub_date` в список полей `fields` '
            'сериализатора модели News'
        )
        assert test_news['author'] == news.author.username, (
            'Проверьте, что `author` сериализатора модели News возвращает '
            'имя пользователя'
        )
        assert test_news['id'] == news.id, (
            f'Проверьте, что при GET запросе на `{url}` возвращается '
            f'корректный список статей'
        )

    @pytest.mark.django_db(transaction=True)
    def test_news_create(self, user_client, user, another_user):
        news_count = News.objects.count()

        data = {}
        response = user_client.post('/v1/news/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на `/v1/posts/` с неправильными '
            'данными возвращается статус 400'
        )

        data = {'text': 'Статья номер 3'}
        response = user_client.post('/v1/news/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `/v1/news/` с правильными '
            'данными возвращается статус 201'
        )
        assert (
                response.json().get('author') is not None
                and response.json().get('author') == user.username
        ), (
            'Проверьте, что при POST запросе на `/v1/news/` автором '
            'указывается пользователь, от имени которого сделан запрос'
        )

        test_data = response.json()
        msg_error = (
            'Проверьте, что при POST запросе на `/v1/news/` возвращается '
            'словарь с данными новой статьи'
        )
        assert type(test_data) == dict, msg_error
        assert test_data.get('text') == data['text'], msg_error

        assert test_data.get('author') == user.username, (
            'Проверьте, что при POST запросе на `/v1/news/` создается статья '
            'от авторизованного пользователя'
        )
        assert news_count + 1 == News.objects.count(), (
            'Проверьте, что при POST запросе на `/v1/news/` создается статья'
        )

    @pytest.mark.django_db(transaction=True)
    def test_news_get_current(self, user_client, news, user):
        response = user_client.get(f'/v1/news/{news.id}/')

        assert response.status_code == 200, (
            'Страница `/v1/news/{id}/` не найдена, проверьте этот адрес '
            'в *urls.py*'
        )

        test_data = response.json()
        assert test_data.get('text') == news.text, (
            'Проверьте, что при GET запросе `/v1/news/{id}/` возвращаете '
            'данные сериализатора, не найдено или неправильное значение `text`'
        )
        assert test_data.get('author') == user.username, (
            'Проверьте, что при GET запросе `/v1/news/{id}/` возвращаете '
            'данные сериализатора, не найдено или не правильное значение '
            '`author`, должно возвращать имя пользователя '
        )

    @pytest.mark.django_db(transaction=True)
    def test_news_patch_current(self, user_client, news, another_news):
        response = user_client.patch(f'/v1/news/{news.id}/',
                                     data={'text': 'Поменяли текст статьи'})

        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/v1/news/{id}/` возвращаете '
            'статус 200'
        )

        test_news = News.objects.filter(id=news.id).first()

        assert test_news, (
            'Проверьте, что при PATCH запросе `/v1/news/{id}/` вы '
            'не удалили статью'
        )

        assert test_news.text == 'Поменяли текст статьи', (
            'Проверьте, что при PATCH запросе `/v1/news/{id}/` вы '
            'изменяете статью'
        )

        response = user_client.patch(f'/v1/news/{another_news.id}/',
                                     data={'text': 'Поменяли текст статьи'})

        assert response.status_code == 403, (
            'Проверьте, что при PATCH запросе `/v1/news/{id}/` для не '
            'своей статьи возвращаете статус 403'
        )

    @pytest.mark.django_db(transaction=True)
    def test_news_delete_current(self, user_client, news, another_news):
        response = user_client.delete(f'/v1/news/{news.id}/')

        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/v1/news/{id}/` возвращаете '
            'статус 204'
        )

        test_news = News.objects.filter(id=news.id).first()

        assert not test_news, (
            'Проверьте, что при DELETE запросе `/v1/news/{id}/` вы '
            'удалили статью'
        )

        response = user_client.delete(f'/v1/news/{another_news.id}/')

        assert response.status_code == 403, (
            'Проверьте, что при DELETE запросе `/v1/news/{id}/` для не своей '
            'статьи возвращаете статус 403'
        )
