#Aquí definirás las rutas (las páginas y funcionalidades de la aplicación).

from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')
