from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "bejelentkezes"

@auth.route('/logout')
def logout():
    return('kijelentkezes')

@auth.route('signup')
def signup():
    return('regisztralas')