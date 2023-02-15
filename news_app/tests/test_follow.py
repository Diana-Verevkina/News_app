import os
import random

import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_app.settings')

name = "test_name23"
password = "hgrewerty567gt"
user = {"username": name, "password": password}
url_user = "http://127.0.0.1:8000/auth/users/"
r_user = requests.post(url_user, data=user)
user_id = r_user.json()["id"]

url_token = "http://127.0.0.1:8000/auth/jwt/create/"
r_token = requests.post(url_token, data=user)
token = r_token.json()["access"]

# second user
name2 = "test_name24"
password2 = "bgvfrty765456uiki"
user2 = {"username": name2, "password": password2}
r_user2 = requests.post(url_user, data=user2)
user2_id = r_user2.json()["id"]

url_follow = "http://127.0.0.1:8000/v1/follow/"


def test_get_follow():
    r = requests.get(url_follow, data=user,
                     headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_post_follow():
    r = requests.post(url_follow, data={"author":name2},
                      headers={'Authorization': 'Bearer ' + token})
    code = 201
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code
