from flask import (Flask, 
        request, url_for, render_template, abort)

app = Flask(__name__)
app.config.from_pyfile("../config.py")

from . import views
from .posts import post_bp
app.register_blueprint(post_bp)

from .users import users_bp
app.register_blueprint(users_bp)