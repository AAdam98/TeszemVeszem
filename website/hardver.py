from flask import Blueprint,render_template
from sqlalchemy.orm import sessionmaker
from models import Advertisement, engine
hardver = Blueprint('hardver', __name__)

Session = sessionmaker(bind=engine)
session = Session()

@hardver.route("/")
def index():
    pickCategory = input()
    advertisements = session.query(Advertisement).all()
    return 'ez az összes hardver', pickCategory, advertisements

@hardver.route("/{pickCategory}")
def index():
    category = 'nemtom'
    filtered_advertisements = session.query(Advertisement).filter_by(category=category).all()
    return 'ez az összes hardver'