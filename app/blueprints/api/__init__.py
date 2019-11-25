from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import User, Post
from app.blueprints.api.forms import racersForm, weatherForm
from flask_login import login_required, current_user
from app import db, login
import requests
import json

bp = Blueprint('api', __name__, template_folder='templates')


@bp.route('/racers', methods=['GET', 'POST'])
@login_required
def racers():
    form = racersForm()
    context = {
        'year': form.year.data,
        'season': form.season.data,
        'form': form,
    }
    if form.validate_on_submit():
        response = requests.get(
            'https://ergast.com/api/f1/' + str(form.year.data) + '/' + str(form.season.data) + '/driverStandings.JSON')
        data = response.json()[
            'MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        context['data'] = data
    return render_template('/api/racers.html', **context)


@bp.route('/weather', methods=['GET', 'POST'])
@login_required
def weather():
    form = weatherForm()
    context = {
        'city_name': form.city_name.data,
        'form': form
    }
    if form.validate_on_submit():
        # with open('data/city_list.json') as cities_file:
        #     cities_data = json.load(cities_file)
        #     city_id = str([city_dict['id'] for city_dict in cities_data if city_dict['name'] == form.city_name.data][0])
        weather_response=requests.get(
            'http://api.openweathermap.org/data/2.5/weather?q=' + str(form.city_name.data) + '&APPID=e90c8358138260940ce42a0e23c95cff')
        data=weather_response.json()
        f_temp = round((data['main']['temp']-273.15) * (9/5) + 32, 1)
        c_temp = round((data['main']['temp']-273.15), 1)
        context['data']=data
        context['f_temp'] = f_temp
        context['c_temp'] = c_temp
    return render_template('/api/weather.html', **context)