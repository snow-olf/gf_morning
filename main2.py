# coding=gbk
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
your_birthday = os.environ['BIRTHDAY']
my_birthday = "04-22"

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  # 实时天气
  url1 = "https://devapi.qweather.com/v7/weather/now?location=101280800&key=b868a6d370af420388d94c105576d9e6"
  res1 = requests.get(url1).json()
  now_weather = res1['now']
  # 预报天气
  url2 = "https://devapi.qweather.com/v7/weather/3d?location=101280800&key=b868a6d370af420388d94c105576d9e6"
  res2 = requests.get(url2).json()
  daily_weather1 = res2['daily'][0]
  daily_weather2 = res2['daily'][1]
  # 空气质量
  url3 = "https://devapi.qweather.com/v7/air/now?location=101280800&key=b868a6d370af420388d94c105576d9e6"
  res3 = requests.get(url3).json()
  air_quality = res3['now']
  
  return now_weather['text'], daily_weather1['tempMin'], daily_weather1['tempMax'], now_weather['temp'], now_weather['feelsLike'], now_weather['humidity'], now_weather['windScale'] + '级' + now_weather['windDir'], air_quality['category'], daily_weather2['textDay'], daily_weather2['tempMin'], daily_weather2['tempMax']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday(birthday):
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
wea, low, high, temperature, feel_temperature, humidity, wind, airQuality, wea_t, low_t, high_t = get_weather()
data = {"city":{"value":city, "color":get_random_color()},
        "weather":{"value":wea, "color":get_random_color()},
        "low":{"value":low, "color":get_random_color()},
        "high":{"value":high, "color":get_random_color()},
        "temperature":{"value":temperature, "color":get_random_color()},
        "feel_temperature":{"value":feel_temperature, "color":get_random_color()},
        "humidity":{"value":humidity, "color":get_random_color()},
        "wind":{"value":wind, "color":get_random_color()},
        "airQuality":{"value":airQuality, "color":get_random_color()},
        "weather_t":{"value":wea_t, "color":get_random_color()},
        "low_t":{"value":low_t, "color":get_random_color()},
        "high_t":{"value":high_t, "color":get_random_color()},
        "love_days":{"value":get_count(), "color":get_random_color()},
        "your_birthday_left":{"value":get_birthday(your_birthday), "color":get_random_color()},
        "my_birthday_left":{"value":get_birthday(my_birthday), "color":get_random_color()},
        "words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
