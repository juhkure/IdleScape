from flask import Flask
from flask import current_app, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from os import path, getenv

app = Flask(__name__)

###################################################################################
# Change run_mode to:                                                             #
# 0 | Normal run from .env variables                                              #
# 1 | Local testing with database creation/modification included                  #
# 2 | Local testing with existing database (with terminal configuration)          #
# 3 | Local testing with existing database instant run (no terminal configuration)#
run_mode = 1                                                                      #
#                                                                                 #
###################################################################################


import routes
