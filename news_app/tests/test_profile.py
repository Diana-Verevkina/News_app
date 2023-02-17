"""import os

import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_app.settings')

name = "testname37"
password = "fghjduyuei892"
user = {"username": name, "password": password}
url_user = "http://127.0.0.1:8000/auth/users/"
r_user = requests.post(url_user, data=user)

url_token = "http://127.0.0.1:8000/auth/jwt/create/"
r_token = requests.post(url_token, data=user)
token = r_token.json()["access"]

url_profile = "http://127.0.0.1:8000/v1/profile/"


def test_post_profile():
    r = requests.post(
        url_profile, data={"first_name": "test_name",
                           "last_name": "test_last_name", "birth_year": 2001,
                           "description": "test description"},
        headers={'Authorization': 'Bearer ' + token}
    )
    code = 201
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code
    global profile_id
    profile_id = str(r.json()["id"]) + "/"


def test_get_profile():
    r = requests.get(url_profile, headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_get_profile_id():
    r = requests.get(url_profile + profile_id,
                     headers={'Authorization': 'Bearer ' + token})
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_put_profile_id():
    r = requests.put(
        url_profile + profile_id, data={"first_name": "test_name_1",
                                        "last_name": "test_last_name_1",
                                        "birth_year": 2001,
                                        "description": "test description"},
        headers={'Authorization': 'Bearer ' + token}
    )
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_patch_profile_id():
    r = requests.patch(
        url_profile + profile_id, data={"first_name": "test_name_2",
                                        "last_name": "test_last_name_2",
                                        "birth_year": 2003,
                                        "description": "test description"},
        headers={'Authorization': 'Bearer ' + token}
    )
    code = 200
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code


def test_delete_profile_id():
    r = requests.delete(
        url_profile + profile_id, headers={'Authorization': 'Bearer ' + token}
    )
    code = 204
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == code
"""