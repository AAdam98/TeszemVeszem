from flask import Blueprint,render_template
hardver = Blueprint('hardver', __name__)

@hardver.route("/index.html", methods=['GET'])
def hardver():
    return render_template('')