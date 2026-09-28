from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from models.user import db, User
from forms.user_forms import RegisterForm, LoginForm, EditProfileForm

user_bp = Blueprint('users', __name__)

# Decorador personalizado para rutas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)
    return decorated_function

# / (GET) - Lista de usuarios
@user_bp.route('/')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

# /register (GET, POST)
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first()
        if existing_user:
            flash('El usuario o correo ya está registrado.', 'danger')
            return render_template('register.html', form=form)

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

# /login (GET, POST)
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Bienvenido de nuevo, {user.username}!', 'success')
            return redirect(url_for('users.user_list'))
        flash('Credenciales incorrectas. Inténtalo de nuevo.', 'danger')
    return render_template('login.html', form=form)

# /logout
@user_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('users.login'))

# /profile/<int:id> (GET)
@user_bp.route('/profile/<int:id>')
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)

# /profile/<int:id>/edit (GET, POST)
@user_bp.route('/profile/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    user = User.query.get_or_404(id)
    if session.get('user_id') != user.id:
        flash('No tienes permiso para editar este perfil.', 'danger')
        return redirect(url_for('users.user_list'))

    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Perfil actualizado con éxito.', 'success')
        return redirect(url_for('users.profile', id=user.id))
    return render_template('edit_profile.html', form=form, user=user)

# /profile/<int:id>/delete (POST)
@user_bp.route('/profile/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if session.get('user_id') != user.id:
        flash('No tienes autorización para eliminar este usuario.', 'danger')
        return redirect(url_for('users.user_list'))

    db.session.delete(user)
    db.session.commit()
    session.clear()
    flash('Usuario eliminado exitosamente.', 'info')
    return redirect(url_for('users.user_list'))
