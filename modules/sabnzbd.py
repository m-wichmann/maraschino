try:
    import json
except ImportError:
    import simplejson as json

from flask import Flask, jsonify, render_template, request
import jsonrpclib, urllib
from jinja2.filters import FILTERS

from Maraschino import app
from maraschino.tools import *


def sab_http():
    if get_setting_value('sabnzbd_https') == '1':
        return 'https://'
    else:
        return 'http://'


def sabnzbd_url_no_api():
    url_base = get_setting_value('sabnzbd_host')
    port = get_setting_value('sabnzbd_port')

    if port:
        url_base = '%s:%s' % (url_base, port)

    return sab_http() + url_base


def sabnzbd_url(mode, extra=""):
    return '%s/api?apikey=%s&mode=%s&output=json%s' % (sabnzbd_url_no_api(), get_setting_value('sabnzbd_api'), mode, extra)


def sab_link():
    SABNZBD_HOST = get_setting_value('sabnzbd_host')
    SABNZBD_PORT = get_setting_value('sabnzbd_port')
    SABNZBD_API = get_setting_value('sabnzbd_api')

    SABNZBD_URL = '%s%s:%s' % (sab_http(), SABNZBD_HOST, SABNZBD_PORT)

    return '%s/api?apikey=%s' % (SABNZBD_URL, SABNZBD_API)


def add_to_sab_link(nzb):
    if get_setting_value('sabnzbd_api') != None:
        return '%s&mode=addurl&name=http://%s&output=json' % (sab_link(), nzb)
    return False

FILTERS['add_to_sab'] = add_to_sab_link


@app.route('/xhr/sabnzbd/')
@app.route('/xhr/sabnzbd/<queue_status>')
@requires_auth
def xhr_sabnzbd(queue_status='hide'):
    old_config = False

    if not get_setting_value('sabnzbd_host'):
        if get_setting_value('sabnzbd_url') != None:
            old_config = True

    downloading = None
    sabnzbd = None
    download_speed = None
    downloading = None

    try:
        result = urllib.urlopen(sabnzbd_url('queue')).read()
        sabnzbd = json.JSONDecoder().decode(result)
        sabnzbd = sabnzbd['queue']

        download_speed = convert_bytes(int((sabnzbd['kbpersec'])[:-3]) * 1024) + '/s'

        if sabnzbd['slots']:
            for item in sabnzbd['slots']:
                if item['status'] == 'Downloading':
                    downloading = item
                    break

    except:
        pass

    return render_template('sabnzbd-queue.html',
        sabnzbd=sabnzbd,
        item=downloading,
        download_speed=download_speed,
        old_config=old_config,
        queue_status=queue_status,
    )


@app.route('/xhr/sabnzbd/queue/<action>/')
@app.route('/xhr/sabnzbd/queue/pause/<time>')
@requires_auth
def sabnzb_queue(action="pause", time=None):
    if not time:
        try:
            result = urllib.urlopen(sabnzbd_url(action)).read()
            sabnzbd = json.JSONDecoder().decode(result)
        except:
            pass
    else:
        try:
            result = urllib.urlopen(sabnzbd_url('config', '&name=set_pause&value=' + time)).read()
            sabnzbd = json.JSONDecoder().decode(result)
        except:
            pass

    if sabnzbd:
        return jsonify({'status': sabnzbd['status']})

    return jsonify({'status': False})


@app.route('/xhr/sabnzbd/speedlimit/<int:speed>/')
@requires_auth
def sabnzb_speed_limit(speed):
    try:
        result = urllib.urlopen(sabnzbd_url('config', '&name=speedlimit&value=%i' % (speed))).read()
        sabnzbd = json.JSONDecoder().decode(result)
        if sabnzbd:
            return jsonify({'status': sabnzbd['status']})
    except:
        pass

    return jsonify({'status': False})


@app.route('/xhr/sabnzbd/individual/<state>/<id>/')
@requires_auth
def sabnzb_individual_toggle(state, id):
    try:
        result = urllib.urlopen(sabnzbd_url('queue', '&name=%s&value=%s' % (state, id))).read()
        sabnzbd = json.JSONDecoder().decode(result)
        if sabnzbd:
            return jsonify({'status': sabnzbd['status']})
    except:
        pass

    return jsonify({'status': False})


@app.route('/sabnzbd/add/', methods=['POST'])
def add_to_sab():
    try:
        url = request.form['url']
    except:
        return jsonify({'error': 'Did not receive URL variable'})

    try:
        return urllib.urlopen(url).read()
    except:
        return jsonify({'error': 'Failed to open URL: %s' % (url)})
