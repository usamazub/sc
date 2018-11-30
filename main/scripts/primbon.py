from django.utils import timezone
from main.models import Data
from enum import Enum

temperature_table = {}
humidity_table = {}

class Tipe(Enum):
    avg_temp = 1
    max_temp = 2
    precipitation = 3
    radiation_time = 4

def to_date(date, delta):
    return date + timezone.timedelta(days=delta)

def construct_temperature_network_probability(data):
    cmp = [1, 2, 4]  # avg_temp, max_temp, precipitation
    for key in range(0, 8):
        dataset = data

        if (key & cmp[0]) != 0:
            dataset = dataset.filter(avg_temp__gte=24)
        elif (key & cmp[0]) == 0:
            dataset = dataset.filter(avg_temp__lt=24)

        if (key & cmp[1]) != 0:
            dataset = dataset.filter(max_temp__gte=26)
        elif (key & cmp[1]) == 0:
            dataset = dataset.filter(max_temp__lt=26)

        if (key & cmp[2]) != 0:
            dataset = dataset.filter(radiation_time__gte=3)
        elif (key & cmp[2]) == 0:
            dataset = dataset.filter(radiation_time__lt=3)

        temperature_table[key] = len(dataset) / len(data)

def construct_humidity_network_probability(data):
    cmp = 1
    for key in range(0, 2):
        dataset = data

        if (key & cmp) != 0:
            dataset = dataset.filter(precipitation__lte=70)
        elif (key & cmp) == 0:
            dataset = dataset.filter(precipitation__gt=70)

        humidity_table[key] = len(dataset) / len(data)


def construct_bayesian_network_probabilities(date):
    data = Data.objects.filter(date__day=date.day, date__month=date.month)

    construct_temperature_network_probability(data)
    construct_humidity_network_probability(data)


def get_raw_data(date, tipe, priority):
    data = Data.objects.filter(date__day=date.day, date__month=date.month)

    sum = 0
    freq = 0

    for dt in data:
        if (
            dt.avg_temp > 8000
            or dt.max_temp > 8000
            or dt.precipitation > 8000
            or dt.radiation_time > 8000
        ):
            continue

        if tipe == Tipe.avg_temp:
            sum += dt.avg_temp
        elif tipe == Tipe.max_temp:
            sum += dt.max_temp
        elif tipe == Tipe.precipitation:
            sum += dt.precipitation
        elif tipe == Tipe.radiation_time:
            sum += dt.radiation_time

        freq += 1

    return priority * sum, priority * freq

def get_temprature_key(avg_temp, max_temp, radiation_time):
    key = 0

    if 22 <= avg_temp < 8000:
        key += 1
    if 26 <= max_temp < 8000:
        key += 2
    if 3 <= radiation_time < 8000:
        key += 4

    return key

def get_temprature_probability(date):
    sum_of_avg_temp , sum_of_max_temp, \
        sum_of_radiation_time = 0, 0, 0
    
    freq_of_avg_temp , freq_of_max_temp, \
        freq_of_radiation_time = 0, 0, 0
    
    for inc in range(0, 10):
        sum_of_avg_temp, freq_of_avg_temp = get_raw_data(
            to_date(date, inc * -365), Tipe.avg_temp, 10 - inc
        )

        sum_of_max_temp, freq_of_max_temp = get_raw_data(
            to_date(date, inc * -365), Tipe.max_temp, 10 - inc
        )


        sum_of_radiation_time, freq_of_radiation_time = get_raw_data(
            to_date(date, inc * -365), Tipe.radiation_time, 10 - inc
        )
    
    expected_avg_temp = sum_of_avg_temp / freq_of_avg_temp
    expected_max_temp = sum_of_max_temp / freq_of_max_temp
    expected_radiation_time = sum_of_radiation_time / freq_of_radiation_time

    return temperature_table[get_temprature_key(
        expected_avg_temp,
        expected_max_temp,
        expected_radiation_time
    )]

def get_humidity_key(precipitation):
    if 0 <= precipitation <= 70:
        return 1
    
    return 0

def get_humidity_probability(date):
    sum_of_precipitation, freq_of_precipitation = 0, 0

    for inc in range(0, 10):
        sum_of_precipitation, freq_of_precipitation = get_raw_data(
            to_date(date, inc * -365), Tipe.precipitation, 10 - inc
        )

    expected_precipitation = sum_of_precipitation / freq_of_precipitation
    
    return humidity_table[get_humidity_key(
        expected_precipitation
    )]

def get_result(duration):
    now = timezone.now()

    for day in range(0, duration):
        construct_bayesian_network_probabilities(to_date(now, day))

        yield get_temprature_probability(to_date(now, day)) * \
            get_humidity_probability(to_date(now, day))

def run(*args):
    get_result(5)
