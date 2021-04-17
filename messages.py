import math

def get_message_about_temp(morning_temp, day_temp, evening_temp, night_temp):
    return 'Утром температура воздуха будет {}℃, днём - {}℃, вечером - {}℃, ночью - {}℃.'.format(
        round(morning_temp), round(day_temp), round(evening_temp), round(night_temp))

def get_message_about_wind(morning_wind_speed, day_wind_speed, evening_wind_speed, night_wind_speed):

    # EMERGENCY HANDLER
    if max(max(morning_wind_speed, day_wind_speed), max(evening_wind_speed, night_wind_speed)) > 33:
        return 'Внимание!!! Сегодня будет ураган!!!'

    # function for convenience
    def get_wind_type(wind_speed):
        if wind_speed < 5:
            return 'слабый'
        elif wind_speed < 14:
            return 'умеренный'
        elif wind_speed < 25:
            return 'сильный'
        else:
            return 'очень сильный'
    
    # get wind types
    avarage_wind_speed = sum([morning_wind_speed, day_wind_speed, evening_wind_speed, night_wind_speed]) / 4
    today_wind_type = get_wind_type(avarage_wind_speed)

    return 'Ветер будет {}. Его средняя скорость будет {} м/c.'.format(today_wind_type, round(avarage_wind_speed))

def get_message_about_weather(morning_weather_by_hours, day_weather_by_hours, evening_weather_by_hours, night_weather_by_hours):

    def get_daypart_weather(daypart_weather_by_hours):
        daypart_weather_forecast = {}

        def add_to_weather_forecast(group):
            if group in daypart_weather_forecast:
                daypart_weather_forecast[group] += 1
            else:
                daypart_weather_forecast[group] = 1

        for weather in daypart_weather_by_hours:
            if weather >= 200 and weather < 300:
                add_to_weather_forecast('гроза')
            elif weather >= 300 and weather < 400 and weather >= 500 and weather < 600:
                add_to_weather_forecast('дождь')
            elif weather >= 600 and weather < 611:
                add_to_weather_forecast('снег')
            elif weather >= 611 and weather < 700:
                add_to_weather_forecast('дождь со снегом')
            elif weather >= 700 and weather < 800:
                add_to_weather_forecast('туман')
            elif weather >= 800 and weather < 804:
                add_to_weather_forecast('безоблачно')
            elif weather == 804:
                add_to_weather_forecast('облачно')

        return daypart_weather_forecast

    morning_weather_forecast = get_daypart_weather(morning_weather_by_hours)
    day_weather_forecast = get_daypart_weather(day_weather_by_hours)
    evening_weather_forecast = get_daypart_weather(evening_weather_by_hours)
    night_weather_forecast = get_daypart_weather(night_weather_by_hours)

    return 'Утром будет {}, днём - {}, вечером - {}, ночью - {}.'.format(
        max(morning_weather_forecast), max(day_weather_forecast), max(evening_weather_forecast), max(night_weather_forecast))