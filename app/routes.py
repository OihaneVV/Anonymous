from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Post
from datetime import datetime
from app.utils import haversine, eliminar_posts_viejos
import uuid

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/post')
@login_required
def post():
    eliminar_posts_viejos()  
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('post.html', posts=posts)

@main.route('/delete_post/<post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(post_id=post_id).first()

    if not post:
        flash('Post no encontrado.', 'error')
        return redirect(url_for('main.post'))

    if post.user_id != current_user.user_id:
        flash('No tienes permiso para eliminar este post.', 'error')
        return redirect(url_for('main.post'))

    db.session.delete(post)
    db.session.commit()
    # flash('Post eliminado correctamente.', 'success')
    return redirect(url_for('main.post'))

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

@main.route('/create_post', methods=['POST'])
@login_required
def create_post():
    text = request.form.get('text')
    lat = request.form.get('lat')
    lon = request.form.get('lon')

    if not text or not lat or not lon:
        flash('Faltan datos para crear el post.', 'error')
        return redirect(url_for('main.post'))

    # Convertir lat y lon a float
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        flash('Coordenadas inválidas.', 'error')
        return redirect(url_for('main.post'))

    new_post = Post(
        post_id=str(uuid.uuid4()),
        user_id=current_user.user_id,
        name=current_user.username,
        text=text,
        lat=lat,
        lon=lon,
        timestamp=datetime.now(),
        likes=0
    )
    db.session.add(new_post)
    db.session.commit()

    # flash('Post creado con éxito!', 'success')
    return redirect(url_for('main.post'))
