from flask import Blueprint, render_template
views = Blueprint('views', __name__)
#Routes
@views.route('/')
def home():
    return render_template("index.html")

@views.route('/rolunk')
def about():
    return render_template("about.html")