from django.shortcuts import render, redirect
from dateutil.rrule import *
from dateutil.parser import *
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
from .forms import GetDataForm, AddStationForm
from weather_project.settings import PROJECT_ROOT
from weatherapp.models import Station


# Create your views here.

def index(request):
    """Function method for weather app"""

    if request.method == 'POST':
        context = getData(request)
    else:
        # form = GetDataForm()
        station_dit = {'KIAHIAWA8': 'Hiawatha', 'KIACEDAR74': 'Cedar Rapids', 'KIAMARIO27': 'Marion'}
        station_obj = Station.objects.all()
        if len(station_obj) == 0:
            for key, value in station_dit.items():
                station_obj = Station(station_name=value, station_id=key)
                station_obj.save()
        form = GetDataForm()
        context = {'form': form}
    return render(request, 'weatherapp/index.html', context)


def addstation(request):
    """Function for add new station """

    if request.method == 'POST':
        form = AddStationForm(request.POST)
        if form.is_valid():
            station_name = form.cleaned_data['addstation']
            add_station = station_name.replace(" ", "_")
            # call api for station id
            url = 'http://api.wunderground.com/api/8a07d3405ae98e3f/geolookup/conditions/q/CA/'+add_station+'.json'
            print(url)
            f = urlopen(url)
            json_string = f.read()
            parsed_json = json.loads(json_string)
            station_id = parsed_json['current_observation']['station_id']
            f.close()

            station_obj = Station(station_name=station_name, station_id=station_id,
                                  station_state='CA')
            station_obj.save()

        return redirect('index')
    else:
        form = AddStationForm()
        context = {'form': form}

        return render(request, 'weatherapp/addstation.html', context)


def getData(request):
    """Function for Get weather data from 'wunderground.com' """

    parameter = request.POST.get('parameter')
    station_id = request.POST.get('stations')
    station = Station.objects.get(station_id=station_id)
    st_name = str(station.station_name).replace(" ", "_")
    st_state = station.station_state
    start_date = str(request.POST.get('start_date'))
    end_date = str(request.POST.get('end_date'))
    api = '8a07d3405ae98e3f'  # developer API key

    # Create list of dates between start and end
    total_days = list(rrule(DAILY, dtstart=parse(start_date.replace("-", "")), until=parse(end_date.replace("-", ""))))

    plot_data = {}
    for day in total_days:
        url = 'http://api.wunderground.com/api/' + api + '/history_' + day.strftime("%Y%m%d") + '/q/'+st_state+'/' + \
              st_name + '.json'
        print(url)
        f = urlopen(url)  # open url and fetch data
        json_string = f.read()
        parsed_json = json.loads(json_string)
        # get observation data
        data = parsed_json['history']['observations']
        # Create list of  Temprature/Humidity
        list1 = list()
        for d in data:
            list1.append(d[parameter])
        f.close()

        plot_data[day] = max(list1)

    img = plotData(plot_data, parameter, start_date, end_date, st_name)  # for ploating data call method 'plotData'
    form = GetDataForm()
    context = {'form': form, 'final_list': plot_data, 'img': img}
    return context


def plotData(data_dict, param, std, end, st_name):
    """Function for ploting graph"""

    figure_name = 'figure.png'
    x_points = []
    y_points = []
    for key, val in data_dict.items():
        x_points.append(key.strftime("%d"))
        if val == 'N/A':
            val = 0
            y_points.append(val)
        else:
            y_points.append(float(val))

    fig = plt.figure()
    plt.xlabel('Dates')
    plt.xticks(range(1, 31))
    plt.title("Weather history for " + st_name+"\nFrom: " + std + " to " + end)
    if param == 'tempm':
        plt.yticks(range(1, 51))
        plt.ylabel('Temprature\n(in celsius)')
        plt.plot(x_points, y_points, '-')
        plt.grid()

    if param == 'hum':
        plt.yticks(range(10, 120, 10))
        plt.ylabel('Humidity\n(in percentage)')
        plt.plot(x_points, y_points, '-', color='g')
        plt.grid()

    fig.savefig(PROJECT_ROOT + 'weatherapp/image/'+figure_name)
    file_name = PROJECT_ROOT + 'weatherapp/image/'+figure_name
    return file_name
