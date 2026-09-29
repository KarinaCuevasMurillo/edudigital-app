from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Usuario

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip().lower()
        contrasena = request.form.get('contrasena', '')
        rol = request.form.get('rol', 'estudiante')

        if not nombre or not correo or not contrasena:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('auth.registro'))

        if Usuario.query.filter_by(correo=correo).first():
            flash('Ya existe una cuenta con ese correo.', 'error')
            return redirect(url_for('auth.registro'))

        nuevo_usuario = Usuario(
            nombre=nombre,
            correo=correo,
            contrasena_hash=generate_password_hash(contrasena),
            rol=rol
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        login_user(nuevo_usuario)
        flash('¡Cuenta creada con éxito!', 'success')

        if rol == 'docente':
            return redirect(url_for('teacher.dashboard'))
        return redirect(url_for('student.diagnostico'))

    return render_template('auth/registro.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        correo = request.form.get('correo', '').strip().lower()
        contrasena = request.form.get('contrasena', '')

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario is None or not check_password_hash(usuario.contrasena_hash, contrasena):
            flash('Correo o contraseña incorrectos.', 'error')
            return redirect(url_for('auth.login'))

        login_user(usuario)

        if usuario.rol == 'docente':
            return redirect(url_for('teacher.dashboard'))
        return redirect(url_for('student.dashboard'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.', 'success')
    return redirect(url_for('auth.login'))