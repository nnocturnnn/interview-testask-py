import datetime

import seaborn as sb

import api


def check_time_cooldown(time: str or None) -> bool:
    if time == None:
        return True 
    time_after_ten_minutes = time + datetime.timedelta(minutes=10)
    return datetime.datetime.now() > time_after_ten_minutes


def exchange_command(message: str) -> str:
    try:
        _, amount, from_currency, _, to_currency = message.split()
        return api.exchange_currencies(from_currency, to_currency, amount)
    except ValueError:
        return "/exchange illegal num argument\nusage: /exchange 10 USD to CAD"


def create_chart(history: dict, message: str, currencys: str) -> str:
    chart = sb.barplot(x=list(history.keys()), y=list(history.values()))
    chart.set_title(currencys)
    chart.set_xlabel("price")
    chart.set_ylabel("date")
    fig = chart.get_figure()
    filename = message.replace("/","") + ".png"
    fig.savefig(filename) 
    return filename


def history_command(message: str) -> str or list:
    try:
        _, currencys, _, num_day, _ = message.split()
        date_end = datetime.datetime.now().date()
        date_start = date_end - datetime.timedelta(days=int(num_day) + 1)
        history = api.exchange_history(currencys.replace("/",""),
             date_start, date_end)
        if isinstance(history, dict):
            return [create_chart(history, message, currencys), message]
        else:
            return history
    except ValueError:
        return "/history illegal num argument\nusage: /history USD/CAD for 7 days"