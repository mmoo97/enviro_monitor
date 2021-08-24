# app/__init__.py

# local imports
from __future__ import print_function
import vars
from datetime import date
import json

# third-party imports
import uuid
from flask import Flask, redirect, url_for, request, render_template, flash, session
from flask_bootstrap import Bootstrap
from envirophat import *

def create_app(config_name):
    app = Flask(__name__) # initialization of the flask app
    Bootstrap(app) # allowing app to use bootstrap

    @app.route('/', methods=['GET', 'POST']) # initial route to display the reg page
    def index():

        # Todo: Make prerec function to get host
        room_id = uuid.uuid1()
        date_list = [date.today().strftime("%Y-%m-%d")]
        hist_temps = [1, 2, 3, 4]

        return render_template('main/base.html', room_id=room_id, date_list=date_list, hist_temps=hist_temps)

    @app.route('/api/temp', methods=['GET'])
    def api_temp():
        return "<h1>{}°C".format(round(weather.temperature(), 2))

    @app.route('/api/all', methods=['GET'])
    def api_all():
        red, green, blue = light.rgb()
        intensity = light.light()
        temp = weather.temperature()
        pressure = weather.pressure()
        heading = motion.heading()

        result = { "light": {
            "color": {
                "red": red,
                "green": green,
                "blue": blue,
            },
            "intensity": intensity,
            },
            "temperature": temp,
            "pressure": pressure,
            "heading": heading,
        }
        return json.dumps(result)

    @app.route('/api/<year>/<month>/<day>', methods=['GET'])
    def api_custom(year, month, day):
        return "<h1>{}, {}, {}".format(year, month, day)

    # misc page error catching
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('error/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('error/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('error/500.html', title='Server Error'), 500

    return app
