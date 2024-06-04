from flask import Blueprint,render_template

Home_rota = Blueprint('Home',__name__)

@Home_rota.route('/')
def index():
    return render_template('landing.html')
