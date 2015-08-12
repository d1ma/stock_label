import os
import sys
import json
from datetime import datetime, timedelta
import logging

#=====[ Flask ]=====
from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import abort
from flask import make_response

#=====[ Model import ]====
from models import *
from auth import requires_auth

#=====[ App/DB setup]=====
static_dir = 'static'
app = Flask(__name__, static_folder=static_dir)


################################################################################
####################[ HANDLING REQUESTS ]#######################################
################################################################################
@app.route("/")
@requires_auth
def dashboard():
    """
    Page: dashboard
    ===============
    List all of the available results
    """
    logging.debug("Getting list_results with %i files" % len(r.tfiles))
    return render_template("list_results.html.jinja2", r=r)

@app.route("/doc/<int:id>")
@requires_auth
def get_file(id):

    f = r.id_to_tfile(id)
    logging.debug("Rendering file %i: %s" % (id, str(r.id_to_tfile(id))))
    return render_template("view_file.html.jinja2", tfile=f, r=r)

@app.route("/model_report")
@requires_auth
def model_report():
    return render_template("model_report.html.jinja2", r=r)
################################################################################
####################[ SERVING STATIC ]##########################################
################################################################################

@app.route("/<static_file>")
def get_static_route(static_file):
    return get_static(static_file)


def get_static(filename):
    return send_from_directory(static_dir, filename)




r = None
if __name__ == '__main__':
    settings.set_up()
    logging.debug("entering main")
    r = main.Main()
    app.run(debug=True)
