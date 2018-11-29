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


def compute_temperature_network_probability(data):
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


def compute_humidity_network_probability(data):
    cmp = 1
    for key in range(0, 2):
        dataset = data

        if (key & cmp) != 0:
            dataset = dataset.filter(precipitation__lte=70)
        elif (key & cmp) == 0:
            dataset = dataset.filter(precipitation__gt=70)

        humidity_table[key] = len(dataset) / len(data)


def compute_bayesian_network_probabilities(date):
    data = Data.objects.filter(date__day=date.day, date__month=date.month)

    compute_temperature_network_probability(data)
    compute_humidity_network_probability(data)


def get_sum_tot(date, tipe):
    data = Data.objects.filter(date__day=date.day, date__month=date.month)

    sum = 0
    tot = 0

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

        tot += 1

    return (sum, tot)


def check_val(date, tipe):
    return get_sum_tot(date, tipe)

def get_result(duration):
    print("fuk")
    date = timezone.now() - timezone.timedelta(days=5 * 30)

    for day in range(0, duration):
        temp = date + timezone.timedelta(days=day)
        compute_bayesian_network_probabilities(temp)

        avg_temp = [0, 0]
        max_temp = [0, 0]
        precipitation = [0, 0]
        radiation_time = [0, 0]

        for inc in range(0, 10):
            temp = to_date(temp, inc * (-365))

            avg_temp = [
                avg_temp[0] + (10 - inc) * check_val(temp, Tipe.avg_temp)[0],
                avg_temp[1] + (10 - inc) * check_val(temp, Tipe.avg_temp)[1],
            ]

            max_temp = [
                max_temp[0] + (10 - inc) * check_val(temp, Tipe.max_temp)[0],
                max_temp[1] + (10 - inc) * check_val(temp, Tipe.max_temp)[1],
            ]

            precipitation = [
                precipitation[0] + (10 - inc) * check_val(temp, Tipe.precipitation)[0],
                precipitation[1] + (10 - inc) * check_val(temp, Tipe.precipitation)[1],
            ]

            radiation_time = [
                radiation_time[0]
                + (10 - inc) * check_val(temp, Tipe.radiation_time)[0],
                radiation_time[1]
                + (10 - inc) * check_val(temp, Tipe.radiation_time)[1],
            ]

            temp = to_date(temp, inc * 365)

        # compute key for temperature
        temperature_key = 0

        avg_temp_val = avg_temp[0] / avg_temp[1]
        max_temp_val = max_temp[0] / max_temp[1]
        radiation_time_val = radiation_time[0] / radiation_time[1]

        if 22 <= avg_temp_val < 8000:
            temperature_key += 1
        if 26 <= max_temp_val < 8000:
            temperature_key += 2
        if 3 <= radiation_time_val < 8000:
            temperature_key += 4

        # compute key for humidity
        humidity_key = 0

        precipitation_val = precipitation[0] / precipitation[1]

        if 0 <= precipitation_val <= 70:
            humidity_key += 1

        print(temperature_table[temperature_key] * humidity_table[humidity_key])
        # yield temperature_table[temperature_key] * humidity_table[humidity_key]


def run(*args):
    get_result(5)
    compute_bayesian_network_probabilities(timezone.now())
