from django import forms
from weatherapp.models import Station


class GetDataForm(forms.Form):
    station_dit = {'KIACEDAR74': 'Cedar Rapids', 'KIABURLI11': 'Burlington', 'KIAMARIO27': 'Marion',
                   'KIACHARI3': 'Chariton', 'KIAMASON5': 'Mason City', 'KIACLINT5': 'Clinton'}

    station_obj = Station.objects.all()
    PARAMETER_CHOICE = [('tempm', 'Temprature'), ('hum', 'Humidity')]
    STATION_CHOICE = list()
    if len(station_obj) == 0:
        for key, value in station_dit.items():
            station_obj = Station(station_name=value, station_id=key)
            station_obj.save()
    else:

        for obj in station_obj:
            STATION_CHOICE.append((obj.station_id, obj.station_name))
    print(station_obj)
    stations = forms.CharField(widget=forms.Select(choices=STATION_CHOICE))
    parameter = forms.CharField(widget=forms.Select(choices=PARAMETER_CHOICE))
    start_date = forms.DateField(required=False)
    end_date = forms.DateField()


class AddStationForm(forms.Form):
    station_dit = {'Burbank': 'CA', 'Hayward': 'CA', 'Los Angeles': 'CA', 'Oakland': 'CA', 'San Jose': 'CA',
                   'San Francisco': 'CA', 'Hiawatha': 'IA'}

    Add_STATION_CHOICE = list()
    for key, val in station_dit.items():
        station_obj = Station.objects.filter(station_name=key).exists()
        if station_obj == False:
            Add_STATION_CHOICE.append((key, key))
    addstation = forms.CharField(widget=forms.Select(choices=Add_STATION_CHOICE))
