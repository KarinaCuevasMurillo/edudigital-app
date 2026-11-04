import random
import string
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Salon, SalonEstudiante, ResultadoQuiz, ProgresoUsuario, Tema
from app.demo import crear_estudiantes_demo, borrar_usuarios_demo

teacher_bp = Blueprint('teacher', __name__, url_prefix='/docente')

MAX_SALONES = 2
DIAS_INACTIVIDAD = 14


def _solo_docentes():
    if current_user.rol != 'docente':
        abort(403)


def generar_codigo_acceso():
    while True:
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Salon.query.filter_by(codigo_acceso=codigo).first():
            return codigo


def estado_estudiante(usuario_id):
    """RF-11: determina si un estudiante va en avance, decadencia o sin actividad reciente."""
    ultimo_resultado = (ResultadoQuiz.query
                         .filter_by(usuario_id=usuario_id)
                         .order_by(ResultadoQuiz.fecha.desc())
                         .first())

    if ultimo_resultado is None:
        return 'sin_actividad'

    dias_desde_ultimo = (datetime.utcnow() - ultimo_resultado.fecha).days
    if dias_desde_ultimo > DIAS_INACTIVIDAD:
        return 'decadencia'  # inactividad prolongada
    if ultimo_resultado.puntaje >= 80:
        return 'avance'
    if ultimo_resultado.puntaje < 50:
        return 'decadencia'
    return 'estable'


@teacher_bp.route('/dashboard')
@login_required
def dashboard():
    _solo_docentes()
    salones = Salon.query.filter_by(docente_id=current_user.id).all()
    return render_template('teacher/dashboard.html', salones=salones, max_salones=MAX_SALONES)


@teacher_bp.route('/salon/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_salon():
    _solo_docentes()

    salones_actuales = Salon.query.filter_by(docente_id=current_user.id).count()
    if salones_actuales >= MAX_SALONES:
        flash(f'Ya alcanzaste el máximo de {MAX_SALONES} salones para esta demostración.', 'error')
        return redirect(url_for('teacher.dashboard'))

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        if not nombre:
            flash('El salón necesita un nombre.', 'error')
            return redirect(url_for('teacher.nuevo_salon'))

        salon = Salon(
            docente_id=current_user.id,
            nombre=nombre,
            codigo_acceso=generar_codigo_acceso()
        )
        db.session.add(salon)
        db.session.commit()

        flash(f'Salón "{nombre}" creado. Código de acceso: {salon.codigo_acceso}', 'success')
        return redirect(url_for('teacher.dashboard'))

    return render_template('teacher/nuevo_salon.html')


@teacher_bp.route('/salon/<int:salon_id>')
@login_required
def ver_salon(salon_id):
    _solo_docentes()
    salon = Salon.query.get_or_404(salon_id)

    if salon.docente_id != current_user.id:
        abort(403)

    inscripciones = SalonEstudiante.query.filter_by(salon_id=salon.id).all()

    estudiantes_info = [
        {'usuario': inscripcion.estudiante, 'estado': estado_estudiante(inscripcion.estudiante.id)}
        for inscripcion in inscripciones
    ]

    # Resumen del grupo: cuántos hay en cada estado y promedio de todos los quizzes
    conteo = {'avance': 0, 'estable': 0, 'decadencia': 0, 'sin_actividad': 0}
    for info in estudiantes_info:
        conteo[info['estado']] += 1

    ids = [i['usuario'].id for i in estudiantes_info]
    puntajes = [r.puntaje for r in ResultadoQuiz.query.filter(ResultadoQuiz.usuario_id.in_(ids)).all()] if ids else []
    promedio = sum(puntajes) / len(puntajes) if puntajes else None

    return render_template('teacher/salon_detalle.html', salon=salon,
                            estudiantes_info=estudiantes_info, conteo=conteo, promedio=promedio)


@teacher_bp.route('/salon/<int:salon_id>/eliminar', methods=['POST'])
@login_required
def eliminar_salon(salon_id):
    _solo_docentes()
    salon = Salon.query.get_or_404(salon_id)

    if salon.docente_id != current_user.id:
        abort(403)

    nombre = salon.nombre
    # Solo se quitan las inscripciones: las cuentas y el progreso de los estudiantes reales se conservan.
    # Los estudiantes ficticios del salón de demostración sí se eliminan por completo.
    inscripciones = SalonEstudiante.query.filter_by(salon_id=salon.id).all()
    usuarios = [i.estudiante for i in inscripciones]
    SalonEstudiante.query.filter_by(salon_id=salon.id).delete()
    db.session.delete(salon)
    db.session.flush()
    borrar_usuarios_demo(usuarios)
    db.session.commit()

    flash(f'Salón "{nombre}" eliminado.', 'success')
    return redirect(url_for('teacher.dashboard'))


@teacher_bp.route('/salon/demo', methods=['POST'])
@login_required
def cargar_demo():
    _solo_docentes()

    if Salon.query.filter_by(docente_id=current_user.id).count() >= MAX_SALONES:
        flash(f'Ya alcanzaste el máximo de {MAX_SALONES} salones. Elimina uno para cargar la demostración.', 'error')
        return redirect(url_for('teacher.dashboard'))

    salon = Salon(docente_id=current_user.id, nombre='Salón de demostración',
                  codigo_acceso=generar_codigo_acceso())
    db.session.add(salon)
    db.session.flush()
    crear_estudiantes_demo(salon)
    db.session.commit()

    flash('Salón de demostración creado con 8 estudiantes ficticios.', 'success')
    return redirect(url_for('teacher.ver_salon', salon_id=salon.id))


@teacher_bp.route('/salon/<int:salon_id>/estudiante/<int:usuario_id>')
@login_required
def ver_estudiante(salon_id, usuario_id):
    _solo_docentes()
    salon = Salon.query.get_or_404(salon_id)
    if salon.docente_id != current_user.id:
        abort(403)

    # El estudiante debe pertenecer a este salón
    inscripcion = SalonEstudiante.query.filter_by(salon_id=salon.id, usuario_id=usuario_id).first_or_404()
    estudiante = inscripcion.estudiante

    progresos = (ProgresoUsuario.query.filter_by(usuario_id=usuario_id)
                 .join(Tema, Tema.id == ProgresoUsuario.tema_id).order_by(Tema.id).all())
    resultados = (ResultadoQuiz.query.filter_by(usuario_id=usuario_id)
                  .order_by(ResultadoQuiz.fecha.asc()).all())
    promedio = sum(r.puntaje for r in resultados) / len(resultados) if resultados else None

    return render_template('teacher/estudiante_detalle.html', salon=salon, estudiante=estudiante,
                            estado=estado_estudiante(usuario_id), progresos=progresos,
                            resultados=resultados, promedio=promedio)
