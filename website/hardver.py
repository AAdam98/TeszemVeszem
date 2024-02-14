from flask import Blueprint,render_template, request
from sqlalchemy.orm import sessionmaker
from models import Advertisement, engine
hardver = Blueprint('hardver', __name__)

Session = sessionmaker(bind=engine)
session = Session()

@hardver.route("/", methods=["GET", "POST"])
def index():
    advertisements = session.query(Advertisement).all()
    return 'ez az összes hardver', advertisements

@hardver.route("/<category>")
def index(category):
    filtered_advertisements = session.query(Advertisement).filter_by(category=category).all()
    return 'ez az összes hardver', filtered_advertisements