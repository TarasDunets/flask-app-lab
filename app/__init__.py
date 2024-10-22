from flask import (Flask, 
        request, url_for, render_template, abort)

app = Flask(__name__)
app.config.from_pyfile("../config.py")

from . import views