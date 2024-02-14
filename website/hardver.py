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

@hardver.route("/<category>", methods=["GET", "POST"])
def query(category, min, max, order):
    if request.method == "POST":
        #szűrés felhasználó által megadott ár alapján 
        query = session.query(Advertisement).filter_by(category=category)
        if min is not None:
            query = query.filter(Advertisement.price >= min)
        if max is not None:
            query = query.filter(Advertisement.price <= max)
        filtered_advertisements = query.all()
        return filtered_advertisements
    
    filtered_advertisements = session.query(Advertisement).filter_by(category=category).all()
    return 'ez az összes hardver', filtered_advertisements