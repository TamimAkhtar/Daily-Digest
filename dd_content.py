import json
from logging import exception
import requests
from urllib import request
from bs4 import BeautifulSoup
from google_trends import daily_trends, realtime_trends
from datetime import datetime,timedelta


def get_random_quote():
    try: 
        URL = 'https://gratefulness.org/practice/word-for-the-day/?gclid=Cj0KCQjwguGYBhDRARIsAHgRm48HsuuXQGx4PVkdjsvEE1HiYlUGIxDH6JWfGTyGDMQG7XmoukqeOJEaAlgrEALw_wcB'
        page = requests.get(URL)
        #print(page.text) 

        soup = BeautifulSoup(page.content , 'html.parser')
        #print(soup.prettify()) 

        for row in soup.findAll('div', attrs={'class' :'content'}):
            quote = row.p.text
        
    except Exception as e:
        quote = 'Always look on the bright side of Life. '
    return quote


def get_weather_forecast(city_name = 'Karachi'):
    try:
        key = 'cad69453783542a3ad5605593c2a4d3e'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key}'
        data = json.load(request.urlopen(url))

        country = data['sys']['country']
        city = data['name']
        condition = data['weather'][0]['description']
        temp = data['main']['temp']

        forecast = {'country' : country,
        'city' : city,
        'condition' : condition,
        'temp' : (f'{round(temp-273.15 , 2)} °C')}
        return forecast
    except Exception as e:
        print(e)
    

def get_google_trends(location = 'FR'):
    try:
        daily_trends(date=None, country='US', language='en-US', timezone='-180')

        today_trends = daily_trends(country=location , language='en-US')
        
        return today_trends
    except Exception as e:
        print(e)
        
def get_wikipedia_article():
    try:
        data = json.load(request.urlopen('https://en.wikipedia.org/api/rest_v1/page/random/summary'))
        return {'title' : data['title'],
        'extract' : data['extract'],
        'Link' : data['content_urls']['desktop']['page']}
    except Exception as e:
        print(e)


if __name__=='__main__':
    ### Test get_random_quote() ###
    print(f'\nTesting Random quote retreival...')
    quote = get_random_quote()
    print(f'-Default quote is..{quote} ')

    ### Test get_weather_forecast() ###
    print(f'\nTesting Weather Forecast retreival...')
    weather = get_weather_forecast()
    city = weather['city']
    country = weather['country']
    condition = weather['condition']
    temp = weather['temp']
    print(f'\n-Weather Forecast for.. {city} , {country} is {condition} with a temperature of {temp}')

    ### Test get_google_trends() ###
    print(f'\nTesting Google Trends retreival...')
    get_google_trends('GB' , 15)
   
   ### Test get_Wikipedia_Article() ###
    print(f'\nTesting Wikipedia Article retreival...')
    article = get_wikipedia_article()
    if article:
        title = article.get('title')
        extract = article.get('extract')
        Link = article.get('Link')
        print(f'\n {title} \n<{Link}>\n{extract}')


