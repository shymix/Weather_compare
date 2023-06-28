import json
import re

import requests
from requests_html import HTMLSession

import side_info


def divide_cities(line) -> list:
    cities = re.split('\W+', line)
    if not cities[-1]:
        cities = cities[:-1]

    print(cities)

    return cities


def get_weather_openweathermap():

    city_weather = {}

    def find_weather(city):

        if city in city_weather:
            return city_weather[city]

        api_url = 'https://api.openweathermap.org/data/2.5/weather'
        request = requests.post(url=api_url, params={'q': city, 'APPID': '599d78f146c2112ff090659d29ea9f35',
                                                     'units': 'metric'})

        if request.status_code == 200:
            response = json.loads(request.content)
            info = side_info.Weather(response['main']['temp'], response['main']['feels_like'],
                                     response['main']['humidity'], response['wind']['speed'])
            city_weather[city] = info
            return city_weather[city]
        return f'I was not able to get the temperature('
    return find_weather


def get_weather_google(city, s: HTMLSession()):
    url = f'https://www.google.com/search?q=weather+{city}'

    r = s.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'})

    temp = r.html.find('span#wob_tm', first=True).text

    feels_like = r.html.find('span#wob_tm', first=True).text

    humidity = r.html.find('span#wob_hm', first=True).text

    wind_speed = r.html.find('span#wob_ws', first=True).text

    return side_info.Weather(temp, feels_like, humidity, wind_speed)


def main():
    session = HTMLSession()
    weather_owm = get_weather_openweathermap()

    line = input('Input 1 city or many cities: ')

    while line != 'end':
        cities = divide_cities(line)

        for city in cities:
            weather_1 = weather_owm(city)
            weather_2 = get_weather_google(city, session)

            result = f'{city}:\nOpen Weather Map: {weather_1}\nGoogle Weather: {weather_2}\n\n'
            print(result)

        line = input("If you want to know more info input other cities. If you want to end input 'end': ")

    print("Good bye :)")


if __name__ == '__main__':
    main()
