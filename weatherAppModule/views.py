
from django.db.models import Q # importing Q for OR queries
from django.urls import reverse # importing reverse for url reverse
from unidecode import unidecode # importing unidecode for word normalization
from django.http import JsonResponse # importing JsonResponse for API response
from django.http import HttpResponseNotFound # importing HttpResponseNotFound for 404 error
from weatherAppModule.models import Cities # importing Cities model
from django.shortcuts import render, redirect # importing render and redirect
import requests  # importing requests for API calls
import pyowm  # importing pyowm to receive weather data
from pyowm.commons.exceptions import *  # importing pyowm exceptions for exception handling
from requests.exceptions import ReadTimeout # importing ReadTimeout for timeout errors
from .utils import error_redirect_url, error_location_url # importing utils


owm = pyowm.OWM('key')  # defining pyowm API key

mgr = owm.weather_manager()  # calling PyOWM weather manager


def get_weather_data(city=None, lat=None, lng=None, name=None): # handling weather data

    if isinstance(city, str):
        observation = mgr.weather_at_place(city)
        city_name = city.title()
    else:
        observation = mgr.weather_at_coords(lat, lng)
        city_name = name

    weather = observation.weather

    sun_times_dict = { # dictionary for sunrise and sunset times
        'twelve_hour': {
            'sunrise': weather.sunrise_time(timeformat='date').strftime("%I:%M%p"),
            'sunset': weather.sunset_time(timeformat='date').strftime("%I:%M%p")
        },
        'twenty_four_hour': {
            'sunrise': weather.sunrise_time(timeformat='date').strftime("%H:%M"),
            'sunset': weather.sunset_time(timeformat='date').strftime("%H:%M")
        }
    }

    celsius_dict = weather.temperature('celsius') 

    fahrenheit_dict = weather.temperature('fahrenheit')

    wind_dict = weather.wind(unit='miles_hour'), 

    celsius_obj = {
        'celsius_temp': int(celsius_dict['temp']),
        'low_celsius': int(celsius_dict['temp_min']),
        'high_celsius': int(celsius_dict['temp_max']),
    }

    fahrenheit_obj = {
        'fahrenheit_temp': int(fahrenheit_dict['temp']),
        'low_fahrenheit': int(fahrenheit_dict['temp_min']),
        'high_fahrenheit': int(fahrenheit_dict['temp_max']),
    }

    def wind_direction(wind):  # returning the wind direction
        compass = {'1': 'N', '2': 'NE', '3': 'E', '4': 'SE', '5': 'S', '6': 'SW', '7': 'W', '8': 'NW'}
        modulo = (wind % 360)
        round = int(modulo / 45) + 1
        return compass[str(round)]
    
    
    def weather_icon(icon):  # returning the weather icon
        att = list(icon.split("/"))
        return att[5][0:3]

    peripheral_data = {
        'humidity': int(weather.humidity),  
        'wind_speed': int(wind_dict[0]['speed']),
        'wind_speed_km': int(wind_dict[0]['speed'] * 1.6),
        'wind_direction': wind_direction(int(wind_dict[0]['deg'])),
        'status': weather.detailed_status,
        'icon': weather_icon(weather.weather_icon_url()),
    }

    city_weather = {
        'city': city_name,
        'celsius_obj': celsius_obj,
        'fahrenheit_obj': fahrenheit_obj,
        'peripheral_data': peripheral_data,
        'sun_times_dict': sun_times_dict
    }

    return city_weather


def search_cities(query): # handling city name filtering

    exact_matches = Cities.objects.filter(normalized_name__iexact=query) # exact matches
    
    # partial matches
    partial_matches = Cities.objects.filter(Q(normalized_name__icontains=query) & ~Q(normalized_name__iexact=query))
    
    return list(exact_matches) + list(partial_matches)


def cities_api(request): # handling cities API

    city = request.GET.get('city')
    payload = []

    if city: # if city is not empty, return city data in defined format

        city_objs = search_cities(city)

        for idx, city_obj in enumerate(city_objs):

            city_dict = {
            "city": city_obj.name,
            "state": city_obj.state,
            "country": city_obj.country,
            "lat": city_obj.lat,
            "lng": city_obj.lng
            }

            payload.append(city_dict)

            if city_obj.state:
                payload[idx]["suggestion"] = "{}, {}, {}".format(city_obj.name, city_obj.state, city_obj.country)
                payload[idx]["normalized_suggestion"] = unidecode("{}, {}, {}".format(city_obj.name, city_obj.state, city_obj.country))
            else:
                payload[idx]["suggestion"] = "{}, {}".format(city_obj.name, city_obj.country)
                payload[idx]["normalized_suggestion"] = unidecode("{}, {}".format(city_obj.name, city_obj.country))
            

    return JsonResponse({'status': 200, 'data': payload,  })


def error_404_view(request, exception=None): # handling 404 error page

    return HttpResponseNotFound(render(request, 'weathersource/page_not_found.html'))


def error_location_view(request, exception=None): # handling location error page

    return HttpResponseNotFound(render(request, 'weathersource/location_not_found.html'))


def home(request, city=None): # handling home page

    if request.method == 'POST': # if request is POST, redirect to search page
        search_query = request.POST.get('search_query', '')
        search_url = reverse('search_city') + f'?city={search_query}'
        return redirect(search_url)

    try:

        def get_client_ip_address(request): # handling client IP address
            req_headers = request.META
            x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for_value:
                ip_addr = x_forwarded_for_value.split(',')[-1].strip()
            else:
                ip_addr = req_headers.get('REMOTE_ADDR')
            return ip_addr

        user_ip = get_client_ip_address(request)

        response = requests.get('https://ipinfo.io/' + user_ip + '?token=d6a18753dde2ed')

        class InvalidIPAddress(Exception): # custom exception class
            "Raised when there's an IP error"
            pass

        try:
            if "error" in response.json():
                raise InvalidIPAddress

        except InvalidIPAddress or ReadTimeout:
            return redirect(error_location_url())
        
        # user_city_info = {
        #     'city': response.json()["city"],
        #     'region': response.json()["region"],
        #     'country': response.json()["country"],
        #     'lat': response.json()["loc"].split(',')[0],
        #     'lng': response.json()["loc"].split(',')[1],
        # }

        # city = str(f'{user_city_info["city"]}, {user_city_info["region"]}, {user_city_info["country"]}')

        # if not user_city_info["region"]:

        #     city = str(f'{user_city_info["city"]}, {user_city_info["country"]}') # uncomment this before upload to pythonanywhere

        # observation = mgr.weather_at_place('Berlin,DE')
        # weather = observation.weather
        # sunrise_sunsets_dict = {
        #     'sunrise_iso': weather.sunrise_time(timeformat='iso'),
        #     'sunrset_iso': weather.sunset_time(timeformat='iso')
        # }

        city = 'Berlin,DE' #comment or delete this before upload to pythonanywhere

        context = {'city_weather': get_weather_data(city), }
        return render(request, 'weathersource/index.html', context)

    except APIRequestError or IndexError or BadGatewayError or NotFoundError or InvalidSSLCertificateError or ValueError:
        return redirect(error_redirect_url())
    


def search_city(request): # handling search page

    search_query = request.GET.get('city', '')
    city_input = str(search_query)
    city_arr = city_input.split(',')
    city = unidecode(str(city_arr[0]))
    normalized_city = unidecode(city_input)

    response = requests.get('http://127.0.0.1:8000/weathersource/api/search?city={}'.format(city))
    data = response.json()

    try:

        lat = ''
        lng = ''

        for item in data['data']:
            if item['normalized_suggestion'] == normalized_city:
                lat = item['lat']
                lng = item['lng']
        if not lat:
            return redirect(error_redirect_url())
        context = { 'city_weather': get_weather_data(None, float(lat), float(lng), city_input), 'search_query': search_query, 'info': city } #(lat, lng)

        return render(request, 'weathersource/index.html', context)

    except APIResponseError or IndexError or BadGatewayError or NotFoundError or InvalidSSLCertificateError or ValueError:
        return redirect(error_redirect_url())
    
