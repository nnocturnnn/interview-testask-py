import requests
import config
import json
import random
import secrets
import string

from rich import print
from datetime import datetime, timedelta
from python_rucaptcha.HCaptcha import aioHCaptcha

def fingerprint() -> str:
    response = requests.post(f"{config.URL_AUTH}/fingerprint")
    if response.status_code == 200:
        print(response.content)
        content: dict = json.loads(response.content)
        return content.get('fingerprint')
    else:
        result = json.loads(response.content)
        raise Exception(result)

def register(fingerprint, captcha_key=None):
    data = {
        'captcha_key': captcha_key,
        'consent': True,
        'date_of_birth': "1988-05-02",
        'email': "********",
        'fingerprint': fingerprint,
        'gift_code_sku_id': None,
        'invite': None,
        'password': "*******",
        'username': "Odling Ziva",
    }

    response = requests.post("https://discord.com/register", json=data)
    print(response)

def random_date():
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2000, 1, 1)
    t: timedelta = end_date - start_date
    rand_days = random.randrange(t.days)
    result = start_date + timedelta(days=rand_days)
    return result.strftime("%Y-%m-%d")

def random_password(lenght=16):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(lenght))