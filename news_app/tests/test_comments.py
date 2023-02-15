"""import os

import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_app.settings')

name = "testname24"
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


def test_get_comments():
    r = requests.get(url_news + news_id + "/comments/",
                      headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_post_comments():
    r = requests.post(url_news + news_id + "/comments/",
                      data={"text": "test comment"},
                      headers={'Authorization': 'Bearer ' + token})
    code = 201
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code

    global comment_id
    comment_id = str(r.json()["id"]) + "/"


def test_get_comments_id():
    r = requests.get(url_news + news_id + "/comments/" + comment_id,
                     headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_put_comments_id():
    r = requests.put(url_news + news_id + "/comments/" + comment_id,
                     data={"text": "test comment 2.0"},
                     headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_patch_comments_id():
    r = requests.patch(url_news + news_id + "/comments/" + comment_id,
                     data={"text": "test comment 3.0"},
                     headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_delete_comments_id():
    r = requests.delete(url_news + news_id + "/comments/" + comment_id,
                        headers={'Authorization': 'Bearer ' + token})
    code = 204
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code
"""