from flask import abort, render_template, request, redirect, url_for
from flask_simplelogin import login_required

@login_required   
def logout():
    session['logged_in'] = False

@login_required
def home():
    return 'Home Flask'