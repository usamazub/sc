import datetime
import requests

from django.utils import timezone

from main.models import Data


URL = 'https://dataonline.bmkg.go.id/data_iklim/get_data'
PROVINCE_ID = '9'  # Kep. Bangka Belitung
REGENCY_ID = '139'  # Kab. Belitung
DEFAULT_START_DATE = datetime.date(2010, 1, 1)
HEADERS = [
    'wmo_id',
    'station',
    'date',
    'min_temp',
    'max_temp',
    'avg_temp',
    'humidity',
    'precipitation',
    'radiation_time',
    'avg_wind_speed',
    'most_wind_direction',
    'max_wind_speed',
    'wind_direction_at_max'
]

def run(*args):
    count = Data.objects.count()

    if count == 0:
        start_date = DEFAULT_START_DATE
    else:
        start_date = Data.objects.first().date + datetime.timedelta(days=1)

    end_date = timezone.localtime().date()

    req = requests.post(URL, data={
        'idrefprovince': PROVINCE_ID,
        'idrefregency': REGENCY_ID,
        'startdate': start_date.strftime('%m/%d/%Y'),
        'enddate': end_date.strftime('%m/%d/%Y')
    })

    items = req.json()['data']
    print(len(items))
    for item in items:
        keys = dict(zip(HEADERS, item))
        keys['date'] = datetime.datetime.strptime(keys.get('date'), '%d-%m-%Y').date()
        Data.objects.create(**keys)
