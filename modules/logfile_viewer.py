from flask import Flask, jsonify, render_template

from maraschino import logger, app, WEBROOT, DATA_DIR
from maraschino.tools import *
import maraschino
 

    
@app.route('/xhr/logfile_viewer/')
@requires_auth
def xhr_logfile_viewer():

    logfile_path = get_setting_value('logfile_viewer_path')
    count = int(get_setting_value('logfile_viewer_count'))

    logfile_lines = []

    try:
        fd = open(logfile_path)
        for line in fd:
            logfile_lines.append(line) 
    except:
        pass

    loglines = logfile_lines[-count:]

    header = "Logfile Viewer: " + str(logfile_path)

    return render_template('logfile_viewer.html',
        header = header,
        loglines = loglines,
    )
