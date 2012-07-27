from flask import Flask, jsonify, render_template
from pywapi.pywapi import get_weather_from_google
import re
import datetime

from maraschino import app
from maraschino.tools import *
import maraschino
 

@app.route('/xhr/pic_frame')
@requires_auth
def xhr_pic_frame():

    pic_frame_img_path = get_setting_value('pic_frame_img_path')
    pic_frame_display_title  = get_setting_value('pic_frame_display_title') == '1'
    pic_frame_img_title = get_setting_value('pic_frame_img_title')
    pic_frame_auto_width  = get_setting_value('pic_frame_auto_width') == '1'
    pic_frame_img_width = get_setting_value('pic_frame_img_width')

    return render_template('pic_frame.html',
        pic_frame_img_path = pic_frame_img_path,
        pic_frame_display_title = pic_frame_display_title,
        pic_frame_img_title = pic_frame_img_title,
        pic_frame_auto_width = pic_frame_auto_width,
        pic_frame_img_width = pic_frame_img_width
    )
