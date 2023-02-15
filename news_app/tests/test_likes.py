import os

import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_app.settings')

name = "testname18"
password = "fghjduyuei892"
user = {"username": name, "password": password}
url_user = "http://127.0.0.1:8000/auth/users/"
requests.post(url_user, data=user)

url_token = "http://127.0.0.1:8000/auth/jwt/create/"
r_token = requests.post(url_token, data=user)
token = r_token.json()["access"]

url_news = "http://127.0.0.1:8000/v1/news/"
r_news = requests.post(url_news, data={"text": "News 2"},
                       headers={'Authorization': 'Bearer ' + token})
news_id = str(r_news.json()["id"])


def test_like():
    r = requests.post(url_news + news_id + "/like/",
                      headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_dislike():
    r = requests.post(url_news + news_id + "/unlike/",
                      headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code