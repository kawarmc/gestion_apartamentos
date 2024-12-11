#Para definir la estructura del modulo
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os

#


load_dotenv()  # Cargar las variables desde .env

# Inicializar las extensiones de Flask
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    # Importar dentro del contexto para evitar imports ciclicos
    from app.models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
    f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # Inicializar la extensión de SQLAlchemy
    db.init_app(app)

    # Otros inicializadores
    bcrypt.init_app(app)
    login_manager.init_app(app)


    from .routes import main
    from .auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    # Imprimir la clave secreta para verificar (sólo en desarrollo, ¡nunca en producción!)
    print(f"SECRET_KEY cargada: {app.config['SECRET_KEY']}")

    return app
