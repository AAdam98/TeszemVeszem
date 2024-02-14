from flask import Blueprint,render_template
hardver = Blueprint('hardver', __name__)

@hardver.route("/")
def index():
    return 'ez az összes hardver'

@hardver.route("/alaplap")
def alaplap():
    return 'alaplap'

@hardver.route("/processzor")
def processzor():
    return 'processzor'

@hardver.route("/memoria")
def memoria():
    return 'memoria'

@hardver.route("/hutes")
def hutes():
    return 'hutes'

@hardver.route("/haz_tap")
def haz_tap():
    return 'haz_tap'

@hardver.route("/jatekvezerlo_szimulator")
def jatekvezerlo_szimulator():
    return 'jatekvezerlo_szimulator'

@hardver.route("/vr")
def vr():
    return 'vr'

@hardver.route("/billentyuzet_eger")
def billentyuzet_eger():
    return 'billentyuzet_eger'

@hardver.route("/egyeb_hardverek")
def egyeb_hardverek():
    return 'egyeb_hardverek'

@hardver.route("/retro_hardverek")
def retro_hardverek():
    return 'retro_hardverek'

@hardver.route("/videokartya")
def videokartya():
    return 'videokartya'

@hardver.route("/monitor")
def monitor():
    return 'monitor'

@hardver.route("/merevlemez_ssd")
def merevlemez_ssd():
    return 'merevlemez_ssd'

@hardver.route("/adathordozo")
def adathordozo():
    return 'adathordozo'

@hardver.route("/halozati_termekek")
def halozati_termekek():
    return 'halozati_termekek'

@hardver.route("/nyomtato_szkenner")
def nyomtato_szkenner():
    return 'nyomtato_szkenner'