from flask import Flask, jsonify, render_template
from pywapi.pywapi import get_weather_from_google
import re
import datetime

from maraschino import app
from maraschino.tools import *
import maraschino
 

@app.route('/xhr/clock')
@requires_auth
def xhr_clock():

    clock_show_date = get_setting_value('clock_show_date') == '1'
    clock_show_time = get_setting_value('clock_show_time') == '1'
    clock_meridian = get_setting_value('clock_meridian') == '1'

    now = datetime.datetime.now()

    date = now.strftime('%A %d %B %Y')

    return render_template('clock.html',
        clock_show_date = clock_show_date,
        clock_show_time = clock_show_time,
        date = date,
        clock_meridian = clock_meridian
    )
