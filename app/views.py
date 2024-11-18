from flask import Flask, request, url_for, render_template, abort
from . import app

@app.route('/')
def hello_world():
    return render_template("base.html")

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return render_template("home.html", agent=agent)

@app.route('/resume') 
def get_resume():
    return render_template("resume.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404