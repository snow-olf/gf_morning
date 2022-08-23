from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY'] + "市南海区"
your_birthday = os.environ['BIRTHDAY']
my_birthday = "04-22"

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id0 = os.environ["USER_ID0"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  # 实时天气
  url1 = "https://devapi.qweather.com/v7/weather/now?location=113.15,23.03&key=b868a6d370af420388d94c105576d9e6"
  res1 = requests.get(url1).json()
  now_weather = res1['now']
  # 预报天气
  url2 = "https://devapi.qweather.com/v7/weather/3d?location=113.15,23.03&key=b868a6d370af420388d94c105576d9e6"
  res2 = requests.get(url2).json()
  daily_weather1 = res2['daily'][0]
  daily_weather2 = res2['daily'][1]
  # 空气质量
  url3 = "https://devapi.qweather.com/v7/air/now?location=113.15,23.03&key=b868a6d370af420388d94c105576d9e6"
  res3 = requests.get(url3).json()
  air_quality = res3['now']
  # 灾害预警
  url4 = "https://devapi.qweather.com/v7/warning/now?location=113.15,23.03&key=b868a6d370af420388d94c105576d9e6"
  res4 = requests.get(url4).json()
  warning = ""
  for x in res4['warning']:
    warning = warning + x['title']
  if warning=="":
    warning = "无灾无险，安详的一天~"
  # 生活指数
  url5 = "https://devapi.qweather.com/v7/indices/1d?type=1,3,9,16&location=113.15,23.03&key=b868a6d370af420388d94c105576d9e6"
  res5 = requests.get(url5).json()
  live_level1 = res5['daily'][0]['category'] + "。" + res5['daily'][0]['text']
  live_level2 = res5['daily'][1]['category'] + "。" + res5['daily'][1]['text']
  live_level3 = res5['daily'][2]['category'] + "。" + res5['daily'][2]['text']
  live_level4 = res5['daily'][3]['category'] + "。" + res5['daily'][3]['text']
  
  return now_weather['text'], daily_weather1['tempMin'], daily_weather1['tempMax'], now_weather['temp'], now_weather['feelsLike'], now_weather['humidity'], now_weather['windScale'] + '级' + now_weather['windDir'], air_quality['category'],  live_level1, live_level2, live_level3, live_level4, warning, daily_weather2['textDay'], daily_weather2['tempMin'], daily_weather2['tempMax']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday(birthday):
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_time():
  year = datetime.now().year
  month = datetime.now().month
  day = datetime.now().day
  weekday = datetime.now().weekday
  week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
  return str(year) + '-' + str(month) + '-' + str(day) + ' ' + week_list[weekday]

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, low, high, temperature, feel_temperature, humidity, wind, airQuality, live_level1, live_level2, live_level3, live_level4, warning, wea_t, low_t, high_t = get_weather()
data = {"time":{"value":get_time(), "color":get_random_color()},
        "city":{"value":city, "color":get_random_color()},
        "weather":{"value":wea, "color":get_random_color()},
        "low":{"value":low, "color":get_random_color()},
        "high":{"value":high, "color":get_random_color()},
        "temperature":{"value":temperature, "color":get_random_color()},
        "feel_temperature":{"value":feel_temperature, "color":get_random_color()},
        "humidity":{"value":humidity, "color":get_random_color()},
        "wind":{"value":wind, "color":get_random_color()},
        "airQuality":{"value":airQuality, "color":get_random_color()},
        "live_level1":{"value":live_level1, "color":get_random_color()},
        "live_level2":{"value":live_level2, "color":get_random_color()},
        "live_level3":{"value":live_level3, "color":get_random_color()},
        "live_level4":{"value":live_level4, "color":get_random_color()},
        "warning":{"value":warning, "color":get_random_color()},
        "weather_t":{"value":wea_t, "color":get_random_color()},
        "low_t":{"value":low_t, "color":get_random_color()},
        "high_t":{"value":high_t, "color":get_random_color()},
        "love_days":{"value":get_count(), "color":get_random_color()},
        "your_birthday_left":{"value":get_birthday(your_birthday), "color":get_random_color()},
        "my_birthday_left":{"value":get_birthday(my_birthday), "color":get_random_color()},
        "words":{"value":get_words(), "color":get_random_color()}}
# res = wm.send_template(user_id, template_id, data)
res = wm.send_template(user_id0, template_id, data)
print(res)