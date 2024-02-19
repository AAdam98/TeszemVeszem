from flask import Blueprint, render_template
from flask_login import login_required, current_user
views = Blueprint('views', __name__)

@views.route('/')
# @login_required
def home():
    return render_template("index.html", user=current_user)

@views.route('/adatlap')
@login_required
def adatlap():
    return 'adatlap'

@views.route('/aboutus')
def aboutus():
    return render_template("about.html")