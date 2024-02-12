from flask import Blueprint,render_template
hardver = Blueprint('hardver', __name__)

@hardver.route("/index.html")
def index():
    return 'ez a hardver'