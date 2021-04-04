from pyowm import OWM
import datetime

owm = OWM('7769486dbc7a1ffcd4ac29ea209fe0a1')
obs = owm.three_hours_forecast("Kyiv")

# def get_daily_forecast():
forecast = obs.get_forecast()
daily_forecast = {}
count = 0
for i in forecast:
    if count < 5 and count > 0:
        # daily_forecast[]

        print(datetime.datetime.fromtimestamp(i.get_reference_time()))
    count += 1



# print(pyowm.__file__)