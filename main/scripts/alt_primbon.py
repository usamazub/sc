from django.utils import timezone
from main.models import Data
from enum import Enum

temperature_table = {}
humidity_table = {}

class Tipe(Enum):
    min_temp = 1
    max_temp = 2
    precipitation = 3
    radiation_time = 4

def to_date(date, delta):
    return date + timezone.timedelta(days=delta)


def compute_temperature_network_probability(data):
    cmp = [1, 2, 4] # min_temp, max_temp, precipitation
    for key in range(0, 8):
        dataset = data

        if (key & cmp[0]) != 0:
            dataset = dataset.filter(min_temp__gte = 22)
        elif (key & cmp[0]) == 0:
            dataset = dataset.filter(min_temp__lt = 22)
        
        if (key & cmp[1]) != 0:
            dataset = dataset.filter(max_temp__gte = 26)
        elif (key & cmp[1]) == 0:
            dataset = dataset.filter(max_temp__lt = 26)
        
        if (key & cmp[2]) != 0:
            dataset = dataset.filter(radiation_time__gte = 3)
        elif (key & cmp[2]) == 0:
            dataset = dataset.filter(radiation_time__lt = 3)

        # print("temperature", key, "=", len(dataset) / len(data))
        temperature_table[key] = len(dataset) / len(data)

def compute_humidity_network_probability(data):
    cmp = 1
    for key in range(0, 2):
        dataset = data

        if (key & cmp) != 0:
            dataset = dataset.filter(precipitation__lte = 70)
        elif (key & cmp) == 0:
            dataset = dataset.filter(precipitation__gt = 70)

        # print("humidity", key, "=", len(dataset) / len(data))
        humidity_table[key] = len(dataset) / len(data)

def compute_bayesian_network_probabilities():
    data = Data.objects.all().filter(min_temp__lte = 8888, 
        max_temp__lte = 8888, precipitation__lte = 8888, 
        humidity__lte = 8888, avg_temp__lte = 8888
    )

    compute_temperature_network_probability(data)
    compute_humidity_network_probability(data)

def get_data(date):
    ret = []

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
        if dt.min_temp > 8000 or dt.max_temp > 8000 \
            or dt.precipitation > 8000 or dt.radiation_time > 8000:
            continue

        if tipe == Tipe.min_temp:
            sum += dt.min_temp
        elif tipe == Tipe.max_temp:
            sum += dt.max_temp
        elif tipe == Tipe.precipitation:
            sum += dt.precipitation
        elif tipe == Tipe.radiation_time:
            sum += dt.radiation_time
        
        tot += 1

    return (sum, tot)

def check_val(date, tipe):
    data = get_data(date)
    temp = get_sum_tot(data, tipe)

    return temp

def get_result(duration):
    date = timezone.now()
    compute_bayesian_network_probabilities()

    probability = 1

    for day in range(0, duration):
        temp = date + timezone.timedelta(days=day)

        min_temp = [0, 0]
        max_temp = [0, 0]
        precipitation = [0, 0]
        radiation_time = [0, 0]

        for inc in range(0, 5):
            temp = to_date(temp, inc*(-365))

            min_temp = [
                min_temp[0] + (5 - inc) * check_val(temp, Tipe.min_temp)[0],
                min_temp[1] + (5 - inc) * check_val(temp, Tipe.min_temp)[1],
            ]

            max_temp = [
                max_temp[0] + (5 - inc) * check_val(temp, Tipe.max_temp)[0],
                max_temp[1] + (5 - inc) * check_val(temp, Tipe.max_temp)[1],
            ]

            precipitation = [
                precipitation[0]
                + (5 - inc) * check_val(temp, Tipe.precipitation)[0],
                precipitation[1]
                + (5 - inc) * check_val(temp, Tipe.precipitation)[1],
            ]

            radiation_time = [
                radiation_time[0]
                + (5 - inc) * check_val(temp, Tipe.radiation_time)[0],
                radiation_time[1]
                + (5 - inc) * check_val(temp, Tipe.radiation_time)[1],
            ]

            temp = to_date(temp, inc*365)
        
        # compute key for temperature
        temperature_key = 0

        min_temp_val = min_temp[0]/min_temp[1]
        max_temp_val = max_temp[0]/max_temp[1]
        radiation_time_val = radiation_time[0]/radiation_time[1]

        # print("min_temp_val", min_temp_val)
        # print("max_temp_val", max_temp_val)
        # print("radiation_time_val", radiation_time_val)

        if 22 <= min_temp_val < 8000:
            temperature_key += 1
        if 26 <= max_temp_val < 8000:
            temperature_key += 2
        if 3 <= radiation_time_val < 8000:
            temperature_key += 4
        
        # compute key for humidity
        humidity_key = 0

        precipitation_val = precipitation[0]/precipitation[1]
        
        # print("precipitation_val", precipitation_val)

        if 0 <= precipitation_val <= 70:
            humidity_key += 1
        
        probability = probability * temperature_table[temperature_key] * humidity_table[humidity_key]

    return probability

def run(*args):
    compute_bayesian_network_probabilities()
    print(get_result(2))
