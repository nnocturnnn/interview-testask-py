import pyowm 
import datetime
import geocoder

owm = pyowm.OWM("7769486dbc7a1ffcd4ac29ea209fe0a1")

def get_owm_now(place):
    if not place:
        g = geocoder.ip('me')
        observation = owm.weather_at_coords(g.latlng[0],g.latlng[1])
        w = observation.get_weather()
    else:
        observation = owm.weather_at_place(place)
        w = observation.get_weather()
    data_dict = {}
    data_dict['time'] = datetime.datetime.fromtimestamp(observation.get_reception_time())
    data_dict['temp'] = w.get_temperature("celsius")
    data_dict['status'] = w.get_detailed_status()
    return data_dict


