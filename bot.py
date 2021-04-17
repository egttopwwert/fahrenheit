import telebot # telegram bot lib
from telebot import types
from tinydb import TinyDB, Query # database lib
import threading

import config # bot's config
import timer # timer
import weather # functions for making requests for WAPI
import messages # function for getting messages about weather forecast

bot = telebot.TeleBot(config.TOKEN) # creating bot
db = TinyDB(config.DATABASE_PATH) # connecting to db

mutex = threading.Lock()

# command /start
@bot.message_handler(commands=['start'])
def welcome(message):
    mutex.acquire()
    try:
        User = Query()
        if db.search(User.id == message.chat.id): # check if user is registered
            bot.send_message(message.chat.id, 'А мы уже знакомы :)')
        else: # if user isn't registred, then...
            bot.send_message(message.chat.id, 'Привет!')
            bot.send_message(message.chat.id, 'Меня зовут Фаренгейт.')
            bot.send_message(message.chat.id, 'Я твой личный "погодный" помощник: подскажу что сегодня одеть, расскажу свежые прогнозы синоптиков и, в случае чего, напомню взять с собой зонтик :)')

            # creating button "Отправить местоположение"
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard = True, row_width = 1, resize_keyboard = True)
            button = types.KeyboardButton(text="Отправить местоположение", request_location=True)
            keyboard.add(button)

            bot.send_message(message.chat.id, 'Чтобы получить информацию о свежайшем прогнозе погоды на сегоднящний день, мне необходимо определить твоё местоположение.', reply_markup=keyboard)
    finally:
        mutex.release()

# treatment of user location
@bot.message_handler(content_types=["location"])
def location(message):
    mutex.acquire()
    try:
        if message.location is None: # if telegram can't find user location
            bot.send_message(message.chat.id, 'К сожалению, я не смог определить твоё местоположение :(')
            bot.send_message(message.chat.id, 'Попробуй меня перезапустить и повтори попытку.')
        else:
            User = Query()
            if not db.search(User.id == message.chat.id): # if user isn't regisered
                db.insert({ 'id': message.chat.id, 'lat': message.location.latitude, 'lon': message.location.longitude})

                hourly_weather_forecast = weather.get_hourly_weather_forecast(message.location.latitude, message.location.longitude)
                [temp, wind_speed, weather_by_hours] = weather.parse_hourly_weather_forecast(hourly_weather_forecast)

                [morning_temp, day_temp, evening_temp, night_temp] = temp
                bot.send_message(message.chat.id, messages.get_message_about_temp(morning_temp, day_temp, evening_temp, night_temp))

                [morning_wind_speed, day_wind_speed, evening_wind_speed, night_wind_speed] = wind_speed
                bot.send_message(message.chat.id, messages.get_message_about_wind(morning_wind_speed, day_wind_speed, evening_wind_speed, night_wind_speed))

                [morning_weather_by_hours, day_weather_by_hours, evening_weather_by_hours, night_weather_by_hours] = [weather_by_hours[0:6], weather_by_hours[6:12], weather_by_hours[12:18], weather_by_hours[18:24]]
                bot.send_message(message.chat.id, messages.get_message_about_weather(morning_weather_by_hours, day_weather_by_hours, evening_weather_by_hours, night_weather_by_hours))
            else:
                bot.send_message(message.chat.id, 'У меня уже есть данные о твоём местоположении.')
    finally:
        mutex.release()

threading.Thread(target=timer.start, args=(bot,)).start() # setup timer
bot.polling()
