import os

import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_app.settings')

# test_user
name = "test_user_1"
password = "fghjduyuei892"
user = {"username": name, "password": password}
url_user = "http://127.0.0.1:8000/auth/users/"
request_user = requests.post(url_user, data=user)

url_token = "http://127.0.0.1:8000/auth/jwt/create/"
r_token = requests.post(url_token, data=user)
token = r_token.json()["access"]