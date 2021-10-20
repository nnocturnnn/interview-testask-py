
import requests

querystring = {"period1":"0","period2":"1634774400"}
r = requests.get("https://finance.yahoo.com/quote/PD/history",params=querystring)
print(r.text)