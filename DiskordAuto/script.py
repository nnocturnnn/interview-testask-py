import sys
import json
import random
import secrets
import string
from datetime import datetime, timedelta

import requests


def get_fingerprint() -> str:
    response = requests.post("https://discord.com/fingerprint")
    if response.status_code == 200:
        content: dict = json.loads(response.content)
        return content.get('fingerprint')
    else:
        result = json.loads(response.content)
        raise Exception(result)


def get_random_date():
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2000, 1, 1)
    t: timedelta = end_date - start_date
    rand_days: int = random.randrange(t.days)
    result = start_date + timedelta(days=rand_days)
    return result.strftime("%Y-%m-%d")


def get_random_password(lenght: int = 16):
    alphabet: str = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(lenght))


def register(email: str, username: str, password: str) -> None:
    date: str = get_random_date()
    fingerprint: str = get_fingerprint()
    captcha_key: str = input("Please input captcha : ")
    data: dict = {
            'captcha_key': captcha_key,
            'consent': True,
            'date_of_birth': date,
            'email': email,
            'fingerprint': fingerprint,
            'gift_code_sku_id': None,
            'invite': None,
            'password': password,
            'username': username,
    }
    headers: dict = {
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    _ = requests.post('https://discord.com/register', json=data,
                      headers=headers)


def get_token(email: str, password: str) -> None:
    headers: dict = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Host': 'discord.com',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Content-Type': 'application/json',
            'Referer': 'https://discord.com/register',
            'Origin': 'https://discord.com',
            'DNT': '1',
            'Connection': 'keep-alive',
        }

    json: dict = {
        'email': email,
        'password': password,
    }
    response = requests.post('https://discord.com/api/v6/auth/login',
                             headers=headers, json=json)
    j_data = response.json()
    print(j_data['token'])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 script.py [email] [username]")
        exit(1)
    _, email, username = sys.argv
    password: str = get_random_password()
    register(email, username, password)
    get_token(email, password)
