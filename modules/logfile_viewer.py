from flask import Flask, jsonify, render_template

from maraschino import logger, app, WEBROOT, DATA_DIR
from maraschino.tools import *
import maraschino
 

    
@app.route('/xhr/logfile_viewer/')
@requires_auth
def xhr_logfile_viewer():

    logfile_path = get_setting_value('logfile_path')

    logline = ""

    try:
        fd = open(logfile_path)
        for line in fd:
            logline = line
            break 
    except:
        pass

    return render_template('logfile_viewer.html',
        logline = logline,
    )
