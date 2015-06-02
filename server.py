import os 
import sys
import json
from datetime import datetime, timedelta

#=====[ Flask ]=====
from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import abort
from flask import make_response

#=====[ Model import ]====
import tagged_file
import featurize
import main
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
    return render_template("list_results.html.jinja2", tfiles=r.tfiles)

@app.route("/doc/<id>")
@requires_auth
def get_file(id):
    return render_template("view_file.html.jinja2", tfile=r.id_to_tfile(id))

################################################################################
####################[ SERVING STATIC ]##########################################
################################################################################

@app.route("/<static_file>")
def get_static_route(static_file):
    return get_static(static_file)



# @app.route("/style.css")
# def get_style():
#     return get_static('style.css')

# @app.route("/select.js")
# def get_select():
#     return get_static("select.js")

# @app.route("/jquery_changes.js")
# def get_jquerychanges():
#     return get_static("jquery_changes.js")


# @app.route("/bootstrap.min.css")
# def get_jquerychanges():
#     return get_static("")


# @app.route("/jquery_changes.js")
# def get_jquerychanges():
#     return get_static("jquery_changes.js")



def get_static(filename):
    return send_from_directory(static_dir, filename)

r = None
if __name__ == '__main__':
    r = main.Main()
    app.run(debug=True)
