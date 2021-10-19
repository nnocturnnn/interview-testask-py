import datetime

import api


def check_time_cooldown(time: datetime) -> bool:
    time_after_ten_minutes = time + datetime.timedelta(minutes=10)
    return datetime.datetime.now > time_after_ten_minutes


def history_command(message: str) -> str:
    try:
        _, amount, from_currency, _, to_currency = message.split()
        return api.exchange_currencies(from_currency, to_currency, amount)
    except ValueError:
        return "/exchange illegal num argument\nusage: /exchange 10 USD to CAD"


history_command("fds sdf")

    # exchange_currencies()
    

def exchange_command(message: str) -> str:
    arguments = message.split()