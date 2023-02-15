"""import os
import random

import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_app.settings')

test_names = ["Mika", "Mira", "Gjudi", "Shura", "Mihailo"]
test_passwords = ["qwertyjnbre4567", "sdrt4567ijhtr", "45654edfghjyuij",
                  "jhgtr5677654rfgh", "njkiko3ksde9k"]

name = test_names[random.randrange(len(test_names))]
password = test_passwords[random.randrange(len(test_passwords))]
user = {"username": name, "password": password}


def test_add_user():
    url = "http://127.0.0.1:8000/auth/users/"
    r = requests.post(url, data=user)
    code = 201
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code

    global user_id
    user_id = r.json()["id"]


def test_jwt_create():
    url = "http://127.0.0.1:8000/auth/jwt/create/"
    r = requests.post(url, data=user)
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code

    global token
    token = r.json()["access"]


def test_login():
    url = "http://127.0.0.1:8000/login/"
    r = requests.post(url, data=user,
                      headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_get_users():
    url = "http://127.0.0.1:8000/auth/users/"
    r = requests.get(url, data=user,
                     headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_get_user_id():
    url = f"http://127.0.0.1:8000/auth/users/{user_id}/"
    r = requests.get(url, data=user,
                     headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_delete_user_id():
    url = f"http://127.0.0.1:8000/auth/users/{user_id}/"
    r = requests.delete(
        url, data={"username": name, "current_password": password},
        headers={'Authorization': 'Bearer ' + token})
    code = 204
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code
"""