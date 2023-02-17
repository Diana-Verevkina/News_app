import pytest

from news.models import Follow


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


class TestFollowAPI:

    @pytest.mark.django_db(transaction=True)
    def test_follow_not_found(self, client, follow_1, follow_2):
        response = client.get('/v1/follow/')

        assert response.status_code != 404, (
            'Страница `/v1/follow/` не найдена, проверьте этот адрес '
            'в *urls.py*'
        )
        assert response.status_code != 500, (
            'Страница `/v1/follow/` не может быть обработана вашим сервером, '
            'проверьте view-функцию в *views.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_follow_not_auth(self, client, follow_1, follow_2):
        response = client.get('/v1/follow/')
        assert response.status_code == 401, (
            'Проверьте, что `/v1/follow/` при GET запросе без токена '
            'возвращает статус 401'
        )

        data = {}
        response = client.post('/v1/follow/', data=data)
        assert response.status_code == 401, (
            'Проверьте, что `/v1/follow/` при POST запросе без токена '
            'возвращает статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_follow_get(self, user_client, user, follow_1, follow_2, follow_3):
        response = user_client.get('/v1/follow/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/v1/follow/` с токеном '
            'авторизации возвращается статус 200'
        )

        test_data = response.json()

        assert type(test_data) == list, (
            'Проверьте, что при GET запросе на `/v1/follow/` возвращается '
            'список'
        )

        assert len(test_data) == Follow.objects.filter(
            author__username=user.username).count(), (
            'Проверьте, что при GET запросе на `/v1/follow/` возвращается '
            'список всех подписчиков пользователя'
        )

        follow = Follow.objects.filter(user=user)[0]
        test_group = test_data[0]
        assert 'user' in test_group, (
            'Проверьте, что добавили `user` в список полей `fields` '
            'сериализатора модели Follow'
        )
        assert 'author' in test_group, (
            'Проверьте, что добавили `author` в список полей `fields` '
            'сериализатора модели Follow'
        )

        assert test_group['user'] == follow.user.username, (
            'Проверьте, что при GET запросе на `/v1/follow/` возвращается '
            'список подписок текущего пользователя, в поле `user` должен '
            'быть `username`'
        )
        assert test_group['author'] == follow.author.username, (
            'Проверьте, что при GET запросе на `/v1/follow/` возвращается '
            'весь список подписок, в поле `author` должен быть `username`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_follow_create(self, user_client, follow_2, follow_3, user, user_2,
                           another_user):
        follow_count = Follow.objects.count()

        data = {}
        response = user_client.post('/v1/follow/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на `/v1/follow/` с неправильными '
            'данными возвращается статус 400'
        )

        data = {'author': another_user.username}
        response = user_client.post('/v1/follow/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `/v1/follow/` с правильными '
            'данными возвращается статус 201'
        )

        test_data = response.json()

        msg_error = (
            'Проверьте, что при POST запросе на `/v1/follow/` возвращается '
            'словарь с данными новой подписки'
        )
        assert type(test_data) == dict, msg_error
        assert test_data.get('user') == user.username, msg_error
        assert test_data.get('author') == data['author'], msg_error

        assert follow_count + 1 == Follow.objects.count(), (
            'Проверьте, что при POST запросе на `/v1/follow/` создается '
            'подписка'
        )

        response = user_client.post('/v1/follow/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на `/v1/follow/` '
            'на уже подписанного автора возвращается статус 400'
        )

        data = {'author': user.username}
        response = user_client.post('/v1/follow/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на `/v1/follow/` '
            'при попытке подписаться на самого себя возвращается статус 400'
        )

    @pytest.mark.django_db(transaction=True)
    def test_follow_search_filter(self, user_client, follow_1, follow_2,
                                  follow_3, follow_4, follow_5,
                                  user, user_2, another_user):

        follow_user = Follow.objects.filter(user=user)
        follow_user_cnt = follow_user.count()

        response = user_client.get('/v1/follow/')
        assert response.status_code != 404, (
            'Страница `/v1/follow/` не найдена, проверьте этот '
            'адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Страница `/v1/follow/` не работает, проверьте view-функцию'
        )

        test_data = response.json()
        assert len(test_data) == follow_user_cnt, (
            'Проверьте, что при GET запросе на `/v1/follow/` возвращается '
            'список всех подписок пользователя'
        )
