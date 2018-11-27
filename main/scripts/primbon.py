from django.utils import timezone
from main.models import Data
from enum import Enum

class Tipe(Enum):
    min_temp = 1
    max_temp = 2
    avg_temp = 3
    humidity = 4
    precipitation = 5
    radiation_time = 6
    avg_wind_speed = 7
    max_wind_speed = 8
    wind_direction_at_max = 9

# kelembapan, curah hujan
# lama penyinaran
# kecepatan anginp 
# arah angin terbanyak
# arah angin terbesar
# arah angin saat kecepatan maksimum
def to_date(date, delta):
    return date + timezone.timedelta(days=delta)

def get_data(date):
    ret = []

    for i in (0, 5):
        date = to_date(date, -i)
        data = Data.objects.filter(date=date)
        date = to_date(date, i)

        for dt in data:
            ret.append(dt)
        

    for i in (0, 5):
        date = to_date(date, -365)

        for j in (0, 3):
            date = to_date(date, j)
            data = Data.objects.filter(date=date)
            date = to_date(date, -j)

            for dt in data:
                ret.append(dt)
            

        for j in (1, 3):
            date = to_date(date, -j)
            data = Data.objects.filter(date=date)
            date = to_date(date, j)

            for dt in data:
                ret.append(dt)
    
    return ret

def get_sum_tot(data, tipe):
    sum = 0
    tot = 0

    for dt in data:
        if tipe == Tipe.min_temp:
            if dt.min_temp > 8000:
                continue
            
            sum += dt.min_temp
            tot += 1
        elif tipe == Tipe.max_temp:
            if dt.max_temp > 8000:
                continue
            
            sum += dt.max_temp
            tot += 1
        elif tipe == Tipe.avg_temp:
            if dt.avg_temp > 8000:
                continue
            
            sum += dt.avg_temp
            tot += 1
        elif tipe == Tipe.humidity:
            if dt.humidity > 8000:
                continue
            
            sum += dt.humidity
            tot += 1
        elif tipe == Tipe.precipitation:
            if dt.precipitation > 8000:
                continue
            
            sum += dt.precipitation
            tot += 1
        elif tipe == Tipe.radiation_time:
            if dt.radiation_time > 8000:
                continue
            
            sum += dt.radiation_time
            tot += 1
        elif tipe == Tipe.avg_wind_speed:
            if dt.avg_wind_speed > 8000:
                continue
            
            sum += dt.avg_wind_speed
            tot += 1
        elif tipe == Tipe.max_wind_speed:
            if dt.max_wind_speed > 8000:
                continue
            
            sum += dt.max_wind_speed
            tot += 1
        elif tipe == Tipe.wind_direction_at_max:
            if dt.wind_direction_at_max > 8000:
                continue
            
            sum += dt.wind_direction_at_max
            tot += 1

    return (sum, tot)

def check_val(date, tipe):
    data = get_data(date)
    temp = get_sum_tot(data, tipe)

    return temp

def get_result(duration):
    date = timezone.now()
    print(date.strftime("%d"), date.strftime("%B"))

    min_temp = [0, 0]
    max_temp = [0, 0]
    avg_temp = [0, 0]
    humidity = [0, 0]
    precipitation = [0, 0]
    radiation_time = [0, 0]
    avg_wind_speed = [0, 0]
    max_wind_speed = [0, 0]
    wind_direction_at_max = [0, 0]

    for inc in range(0, duration):
        temp = date + timezone.timedelta(days=inc)

        min_temp = [
            min_temp[0] + check_val(temp, Tipe.min_temp)[0],
            min_temp[1] + check_val(temp, Tipe.min_temp)[1]
        ]

        max_temp = [
            max_temp[0] + check_val(temp, Tipe.max_temp)[0],
            max_temp[1] + check_val(temp, Tipe.max_temp)[1]
        ]

        avg_temp = [
            avg_temp[0] + check_val(temp, Tipe.avg_temp)[0],
            avg_temp[1] + check_val(temp, Tipe.avg_temp)[1]
        ]

        humidity = [
            humidity[0] + check_val(temp, Tipe.humidity)[0],
            humidity[1] + check_val(temp, Tipe.humidity)[1]
        ]

        precipitation = [
            precipitation[0] + check_val(temp, Tipe.precipitation)[0],
            precipitation[1] + check_val(temp, Tipe.precipitation)[1]
        ]

        radiation_time = [
            radiation_time[0] + check_val(temp, Tipe.radiation_time)[0],
            radiation_time[1] + check_val(temp, Tipe.radiation_time)[1]
        ]

        avg_wind_speed = [
            avg_wind_speed[0] + check_val(temp, Tipe.avg_wind_speed)[0],
            avg_wind_speed[1] + check_val(temp, Tipe.avg_wind_speed)[1]
        ]

        max_wind_speed = [
            max_wind_speed[0] + check_val(temp, Tipe.max_wind_speed)[0],
            max_wind_speed[1] + check_val(temp, Tipe.max_wind_speed)[1]
        ]

        wind_direction_at_max = [
            wind_direction_at_max[0] + check_val(temp, Tipe.wind_direction_at_max)[0],
            wind_direction_at_max[1] + check_val(temp, Tipe.wind_direction_at_max)[1]
        ]

    return {}

def run(*args):
    print(get_result(2))