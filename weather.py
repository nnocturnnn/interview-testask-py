import pyowm 
import geocoder
import os

# owm = pyowm.OWM(os.getenv('API_WEATHER')) 
owm = pyowm.OWM("7769486dbc7a1ffcd4ac29ea209fe0a1")

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def get_owm_now(place):
    if not place:
        g = geocoder.ip('me')
        observation = owm.weather_at_coords(g.latlng[0],g.latlng[1])
        w = observation.get_weather()
    else:
        observation = owm.weather_at_place(place)
        w = observation.get_weather()
    data_dict = {}
    data_dict['time'] = observation.get_reception_time('date')
    data_dict['temp'] = w.get_temperature("celsius")
    for key in data_dict['temp']:
        try:
            data_dict['temp'][key] = toFixed(data_dict['temp'][key],1)
        except:
            continue
    data_dict['status'] = w.get_detailed_status()
    return data_dict

def get_own_three_hour(place):
    if not place:
        g = geocoder.ip('me')
        observation = owm.three_hours_forecast_at_coords(g.latlng[0],g.latlng[1])
        forecast = observation.get_forecast()
    else:
        observation = owm.three_hours_forecast(place)
        forecast = observation.get_forecast()
    list_wether = []
    for i in forecast:
        data_list = []
        data_list.append(i.get_reference_time('date').strftime("%H:%M"))
        data_list.append(i.get_temperature("celsius"))
        for key in data_list[1]:
            try:
                data_list[1][key] = toFixed(data_list[1][key],1)
            except:
                continue
        data_list.append(i.get_detailed_status())
        list_wether.append(data_list)
    return list_wether
        
    