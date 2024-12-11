from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.models import User
from app.forms import RegistrationForm, LoginForm
from app import db, bcrypt
import re  # Importamos re para la validación de contraseñas

auth = Blueprint('auth', __name__)

# Función para validar contraseñas fuertes
def validar_contraseña(contraseña):
    """
    Verifica si una contraseña cumple con los requisitos de seguridad.
    """
    if len(contraseña) < 8:
        return "La contraseña debe tener al menos 8 caracteres."
    if not any(char.isupper() for char in contraseña):
        return "La contraseña debe contener al menos una letra mayúscula."
    if not any(char.islower() for char in contraseña):
        return "La contraseña debe contener al menos una letra minúscula."
    if not any(char.isdigit() for char in contraseña):
        return "La contraseña debe contener al menos un número."
    if not any(char in "!@#$%^&*()-_=+[]{};:,.<>?/|`~" for char in contraseña):
        return "La contraseña debe contener al menos un carácter especial."
    return None

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Validar la contraseña antes de continuar
        mensaje_error = validar_contraseña(form.password.data)
        if mensaje_error:
            flash(mensaje_error, 'danger')
            return render_template('register.html', form=form)
        
        # Si la contraseña es válida, continúa con el registro
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html', form=form)
