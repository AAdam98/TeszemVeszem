from flask import Blueprint, render_template
views = Blueprint('views', __name__)
#Routes
@views.route('/')
def home():
    return render_template("home.html")

@views.route("/alaplap")
def alaplap():
    return 'alaplap'

@views.route("/processzor")
def processzor():
    return 'processzor'

@views.route("/memoria")
def memoria():
    return 'memoria'

@views.route("/hutes")
def hutes():
    return 'hutes'

@views.route("/haz_tap")
def haz_tap():
    return 'haz_tap'

@views.route("/jatekvezerlo_szimulator")
def jatekvezerlo_szimulator():
    return 'jatekvezerlo_szimulator'

@views.route("/vr")
def vr():
    return 'vr'

@views.route("/billentyuzet")
def billentyuzet():
    return 'billentyuzet'

@views.route("/eger")
def eger():
    return 'eger'

@views.route("/egyeb_hardverek")
def egyeb_hardverek():
    return 'egyeb_hardverek'

@views.route("/retro_hardverek")
def retro_hardverek():
    return 'retro_hardverek'

@views.route("/videokartya")
def videokartya():
    return 'videokartya'

@views.route("/monitor")
def monitor():
    return 'monitor'

@views.route("/merevlemez_ssd")
def merevlemez_ssd():
    return 'merevlemez_ssd'

@views.route("/adathordozo")
def adathordozo():
    return 'adathordozo'

@views.route("/halozati_termekek")
def halozati_termekek():
    return 'halozati_termekek'

@views.route("/nyomtato_szkenner")
def nyomtato_szkenner():
    return 'nyomtato_szkenner'