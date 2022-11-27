from flask import Blueprint, render_template, request, url_for, flash, redirect, jsonify
from flask_login import login_required, current_user
from dotenv import load_dotenv
from .models import City
from . import db
import requests
import os

load_dotenv()

views = Blueprint('views', __name__)

API_KEY = os.getenv("API_KEY")

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=imperial&appid={ API_KEY }'
    res = requests.get(url).json()
    return res


@views.route('/', methods=['GET'])
@login_required
def home_get():
    print(current_user.id)
    cities = City.query.all()
        
    weather_data = []
    for city in cities:    
        res = get_weather_data(city.name)
            
        weather = {
            'city': city.name,
            'temperature': res['main']['temp'],
            'description': res['weather'][0]['description'],
            'icon': res['weather'][0]['icon'],
        }

        weather_data.append(weather)
        
    return render_template("home.html", user=current_user, weather_data=weather_data)    


@views.route('/', methods=['POST'])
@login_required
def home_post():
        new_city = request.form.get('city')

        if new_city:
            existing_city = City.query.filter_by(name=new_city, user_id=current_user.id).first()
            
        if not existing_city:
            new_city_data = get_weather_data(new_city)
            
            if new_city_data['cod'] == 200:
                new_city_obj = City(name=new_city, user_id=current_user.id)
                db.session.add(new_city_obj)
                db.session.commit()
                flash('City added to list', category='success')

            else:
                flash('City does not exist in the world!', category='error')
        else:
            flash('City already exists in the database!', category='error')
                
        return redirect(url_for('views.home_get'))
    

@views.route('/delete/<name>')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Successfully deleted { city.name }', 'success')
    return redirect(url_for('views.home_get'))