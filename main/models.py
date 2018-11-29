from django.db import models

class Data(models.Model):
    wmo_id = models.CharField(max_length=16)
    station = models.CharField(max_length=128)
    date = models.DateField()
    min_temp = models.FloatField()
    max_temp = models.FloatField()
    avg_temp = models.FloatField()
    humidity = models.FloatField()
    precipitation = models.FloatField()
    radiation_time = models.FloatField()
    avg_wind_speed = models.FloatField()
    most_wind_direction = models.CharField(max_length=8)
    max_wind_speed = models.FloatField()
    wind_direction_at_max = models.FloatField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return '{} {}'.format(self.wmo_id, self.date)
