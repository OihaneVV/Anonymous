from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/post')
@login_required
def post():
    return render_template('post.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.post'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash('Nombre o contraseña incorrectos.')
            return render_template('index.html')

        login_user(user)
        return redirect(url_for('main.post'))

    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    # Si ya está logueado, lo mandamos al index
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validar que los campos no estén vacíos
        if not username or not password:
            flash('Por favor, rellena todos los campos.')
            return render_template('register.html')

        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Nombre ya registrado. Usa otro.')
            return render_template('register.html')

        # Crear usuario nuevo y guardar en BD
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registro correcto. Ya puedes iniciar sesión.')
        return redirect(url_for('main.index'))  # Aquí vas a index, que puede ser login

    # GET muestra el formulario
    return render_template('register.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.')
    return redirect(url_for('main.index'))


