from flask import Blueprint,render_template, request
from sqlalchemy.orm import sessionmaker
from .models import Advertisement, engine
hirdetes = Blueprint('hirdetes', __name__)
Session = sessionmaker(bind=engine)
session = Session()

@hirdetes.route("/<order>/<orderBy>", methods=["GET", "POST"])
def index(order, orderBy):
    # összes hírdetés sorba rendezése
    if request.method == "POST":
        if orderBy == "Ár":
            if order == "Csökkenő":
                sorted_advertisements = session.query(Advertisement).order_by(Advertisement.price.desc()).all()
            elif order == "Növekvő":
                sorted_advertisements = session.query(Advertisement).order_by(Advertisement.price.asc()).all()

        elif orderBy == "Dátum":
            if order == "Csökkenő":
                sorted_advertisements = session.query(Advertisement).order_by(Advertisement.date.desc()).all()
            elif order == "Növekvő":
                sorted_advertisements = session.query(Advertisement).order_by(Advertisement.date.asc()).all()

        return sorted_advertisements

    # összes hirdetés
    advertisements = session.query(Advertisement).all()
    return advertisements

@hirdetes.route("/<category>", methods=["GET", "POST"])
def query(category, min, max, order, orderBy):
    if request.method == "POST":
        # szűrés felhasználó által megadott ár alapján 
        query = session.query(Advertisement).filter_by(category=category)
        done = False
        if min is not None:
            query = query.filter(Advertisement.price >= min)
            done = True
        elif max is not None:
            query = query.filter(Advertisement.price <= max)
            done = True
        if done:
            filtered_advertisements = query.all()
            return filtered_advertisements
        
        # szűrés a felhasználótól sorba rendezés alapján adott kategóriában
        if orderBy == "Ár":
            if order == "Csökkenő":
                sorted_advertisements = session.query(Advertisement).filter_by(category=category).order_by(Advertisement.price.desc()).all()
            elif order == "Növekvő":
                sorted_advertisements = session.query(Advertisement).filter_by(category=category).order_by(Advertisement.price.asc()).all()
            
        elif orderBy == "Dátum":
            if order == "Csökkenő":
                sorted_advertisements = session.query(Advertisement).filter_by(category=category).order_by(Advertisement.date.desc()).all()
            elif order == "Növekvő":
                sorted_advertisements = session.query(Advertisement).filter_by(category=category).order_by(Advertisement.date.asc()).all()
        return sorted_advertisements
    
    # redirecteket MEG KELL CSINÁLNI
            
    # összes hirdetés egy adott kategóriában
    filtered_advertisements = session.query(Advertisement).filter_by(category=category).all()
    return 'ez az összes hardver', filtered_advertisements