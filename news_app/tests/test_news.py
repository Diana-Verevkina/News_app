"""import os

import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_app.settings')

name = "testname10"
password = "fghjduyuei892"
user = {"username": name, "password": password}
url_user = "http://127.0.0.1:8000/auth/users/"
r_user = requests.post(url_user, data=user)

url_token = "http://127.0.0.1:8000/auth/jwt/create/"
r_token = requests.post(url_token, data=user)
token = r_token.json()["access"]

url_news = "http://127.0.0.1:8000/v1/news/"


def test_get_news():
    r = requests.get(url_news, headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_post_news():
    r = requests.post(url_news, data={"text": "News 1"},
                      headers={'Authorization': 'Bearer ' + token})
    code = 201
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code

    global news_id
    news_id = str(r.json()["id"]) + "/"


def test_get_news_id():
    r = requests.get(url_news + news_id,
                     headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_put_news_id():
    r = requests.put(url_news + news_id, data={"text": "News 1.0"},
                     headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_patch_news_id():
    r = requests.patch(url_news + news_id, data={"text": "News 2.0"},
                       headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_delete_news_id():
    r = requests.delete(url_news + news_id,
                        headers={'Authorization': 'Bearer ' + token})
    code = 204
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code
"""