import datetime
from main.models import Data

# suhu (min, mean, max)
# kelembapan, curah hujan
# lama penyinaran
# kecepatan angin
# arah angin terbanyak
# arah angin terbesar
# arah angin saat kecepatan maksimum

# 5 hari belakang
# hari ini 5 tahun (5 hari -> 2 hari setelah, 2 hari sebelum)
def check_min_temp(date):
    ...

def check_max_temp(date):
    ...

def check_avg_temp(date):
    ...

def check_precipitation(date):
    ...

def check_radiation_time(date):
    ...

def check_avg_wind_speed(date):
    ...

def check_most_wind_direction(date):
    ...

def check_max_wind_speed(date):
    ...

def check_wind_direction_at_max(date):
    ...

def get_result(duration):
    date = datetime.datetime.now()
    print(date.strftime("%d"), date.strftime("%B"))

    ret = 1

    for inc in range(0, duration):
        temp = date + datetime.timedelta(days=inc)
        
        res = 1
        
        res *= check_min_temp(temp) * check_max_temp(temp) * check_avg_temp(temp)
        res *= check_humidity(temp) * check_precipitation(temp)
        res *= check_radiation_time(temp) * check_avg_wind_speed(temp)
        res *= check_most_wind_direction(temp) * check_max_wind_speed(temp)
        res *= check_wind_direction_at_max(temp)

    return {}
