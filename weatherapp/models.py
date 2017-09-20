from django.db import models

# Create your models here.


class Station(models.Model):
    station_name = models.CharField(max_length=200)
    station_id = models.CharField(max_length=10)
    station_state = models.CharField(max_length=200, default="IA")
    def __str__(self):
        return self.station_name
