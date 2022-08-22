from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://t.weather.sojson.com/api/weather/city/101280800" #·ðÉ½´úÂë101280800
  res = requests.get(url).json()
  weather = res['data']
  weather_t0 = res['data']['list'][0]
  weather_t1 = res['data']['list'][1]
  return weather_t0['type'], math.floor(weather_t0['low']), math.floor(weather_t0['high']), math.floor(weather['wendu']), weather['shidu'], weather_t0['fx']+weather_t0['fl'], weather['quality'], math.floor(weather_t1['low']), math.floor(weather_t1['high'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, low, high, temperature, humidity, wind, airQuality, low_t, high_t = get_weather()
data = {"city":{"value":city, "color":get_random_color()},
        "weather":{"value":wea, "color":get_random_color()},
        "low":{"value":low, "color":get_random_color()},
        "high":{"value":high, "color":get_random_color()},
        "temperature":{"value":temperature, "color":get_random_color()},
        "humidity":{"value":humidity, "color":get_random_color()},
        "wind":{"value":wind, "color":get_random_color()},
        "airQuality":{"value":airQuality, "color":get_random_color()},
        "low_t":{"value":low_t, "color":get_random_color()},
        "high_t":{"value":high_t, "color":get_random_color()},
        "love_days":{"value":get_count(), "color":get_random_color()},
        "birthday_left":{"value":get_birthday(), "color":get_random_color()},
        "words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)