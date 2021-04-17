from datetime import datetime # lib for getting time
from threading import Lock # mutex
import time # lib for delays
from tinydb import TinyDB

import weather # functions for making requests for WAPI
import messages # function for getting messages about weather forecast

import config # bot's config

db = TinyDB(config.DATABASE_PATH)
mutex = Lock()

def timer(t, action):
    # function for convenience
    def get_current_time():
        return datetime.now().strftime("%H:%M:%S"); # e.g. 07:41:19
        
    # getting current time
    now = get_current_time()
        
    while now != t:
        # print(now) # for debug
        time.sleep(1) # waiting for 1 second
        now = get_current_time() 
        
    action() # starting action

# function for sending daily weather info
def send_daily_weather_info(bot_instance):
    mutex.acquire()
    try:
        for user in db:
            user_id, user_lat, user_lon = user['id'], user['lat'], user['lon']

            hourly_weather_forecast = weather.get_hourly_weather_forecast(user_lat, user_lon)
            [temp, wind_speed, weather_by_hours] = weather.parse_hourly_weather_forecast(hourly_weather_forecast)

            bot_instance.send_message(user_id, "Доброе утро!")

            [morning_temp, day_temp, evening_temp, night_temp] = temp
            bot_instance.send_message(user_id, messages.get_message_about_temp(morning_temp, day_temp, evening_temp, night_temp))

            [morning_wind_speed, day_wind_speed, evening_wind_speed, night_wind_speed] = wind_speed
            bot_instance.send_message(user_id, messages.get_message_about_wind(morning_wind_speed, day_wind_speed, evening_wind_speed, night_wind_speed))

            [morning_weather_by_hours, day_weather_by_hours, evening_weather_by_hours, night_weather_by_hours] = [weather_by_hours[0:6], weather_by_hours[6:12], weather_by_hours[12:18], weather_by_hours[18:24]]
            bot_instance.send_message(user_id, messages.get_message_about_weather(morning_weather_by_hours, day_weather_by_hours, evening_weather_by_hours, night_weather_by_hours))
    finally:
        mutex.release()

# function for daily sending messages
def start(bot_instance):
    while True:
        timer('06:00:00', lambda: send_daily_weather_info(bot_instance)) # waiting for 6 a.m. and then sending daily weather info
