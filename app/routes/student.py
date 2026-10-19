import random
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Materia, Tema, PreguntaDiagnostico, PreguntaQuiz, Recurso, ResultadoQuiz, ProgresoUsuario, Salon, SalonEstudiante
student_bp = Blueprint('student', __name__, url_prefix='/estudiante')


@student_bp.before_request
@login_required
def _solo_estudiantes():
    if current_user.rol == 'docente':
        return redirect(url_for('teacher.dashboard'))

NIVELES = ['basico', 'intermedio', 'avanzado']


def calcular_nivel_por_porcentaje(porcentaje):
    """Regla simple de clasificación inicial (sin IA)."""
    if porcentaje >= 80:
        return 'avanzado'
    elif porcentaje >= 50:
        return 'intermedio'
    return 'basico'


def siguiente_nivel(nivel_actual):
    idx = NIVELES.index(nivel_actual)
    if idx < len(NIVELES) - 1:
        return NIVELES[idx + 1]
    return nivel_actual  # ya está en el nivel más alto


def nivel_anterior(nivel_actual):
    idx = NIVELES.index(nivel_actual)
    if idx > 0:
        return NIVELES[idx - 1]
    return nivel_actual  # ya está en el nivel más bajo


@student_bp.route('/dashboard')
@login_required
def dashboard():
    progresos = ProgresoUsuario.query.filter_by(usuario_id=current_user.id).all()
    salones = (Salon.query.join(SalonEstudiante, SalonEstudiante.salon_id == Salon.id)
               .filter(SalonEstudiante.usuario_id == current_user.id).all())
    return render_template('student/dashboard.html', progresos=progresos, salones=salones)


@student_bp.route('/diagnostico', methods=['GET', 'POST'])
@login_required
def diagnostico():
    if request.method == 'GET':
        materias = Materia.query.all()
        return render_template('student/diagnostico_inicio.html', materias=materias)

    # POST: el usuario eligió una materia, mostramos/evaluamos preguntas
    materia_id = request.form.get('materia_id')

    if materia_id and 'respuestas_enviadas' not in request.form:
        # Paso 1: se eligió la materia -> mostrar preguntas
        materia = Materia.query.get_or_404(materia_id)
        temas = Tema.query.filter_by(materia_id=materia.id).all()

        preguntas = []
        for tema in temas:
            preguntas_tema = PreguntaDiagnostico.query.filter_by(tema_id=tema.id).all()
            if preguntas_tema:
                preguntas.append(random.choice(preguntas_tema))

        return render_template('student/diagnostico_preguntas.html',
                                materia=materia, preguntas=preguntas)

    # Paso 2: se enviaron las respuestas -> calificar y asignar nivel
    materia_id = request.form.get('materia_id')
    materia = Materia.query.get_or_404(materia_id)
    temas = Tema.query.filter_by(materia_id=materia.id).all()

    correctas = 0
    total = 0
    for tema in temas:
        pregunta_id = request.form.get(f'pregunta_tema_{tema.id}')
        respuesta = request.form.get(f'respuesta_tema_{tema.id}')
        if pregunta_id:
            total += 1
            pregunta = PreguntaDiagnostico.query.get(int(pregunta_id))
            if pregunta and respuesta == pregunta.respuesta_correcta:
                correctas += 1

    porcentaje = (correctas / total * 100) if total else 0
    nivel_inicial = calcular_nivel_por_porcentaje(porcentaje)

    for tema in temas:
        progreso_existente = ProgresoUsuario.query.filter_by(
            usuario_id=current_user.id, tema_id=tema.id).first()
        if progreso_existente is None:
            db.session.add(ProgresoUsuario(
                usuario_id=current_user.id,
                tema_id=tema.id,
                nivel_actual=nivel_inicial,
                estado='en_curso'
            ))
        else:  # repetir el diagnóstico reasigna el nivel
            progreso_existente.nivel_actual = nivel_inicial
            progreso_existente.estado = 'en_curso'
    db.session.commit()

    flash(f'Diagnóstico completado: {porcentaje:.0f}% de aciertos. '
          f'Nivel inicial asignado: {nivel_inicial}.', 'success')
    return redirect(url_for('student.dashboard'))


@student_bp.route('/tema/<int:tema_id>')
@login_required
def ver_tema(tema_id):
    tema = Tema.query.get_or_404(tema_id)
    progreso = ProgresoUsuario.query.filter_by(
        usuario_id=current_user.id, tema_id=tema_id).first_or_404()

    recursos = Recurso.query.filter_by(
        tema_id=tema_id, nivel=progreso.nivel_actual).all()

    return render_template('student/tema.html',
                            tema=tema, progreso=progreso, recursos=recursos)


@student_bp.route('/tema/<int:tema_id>/quiz', methods=['GET', 'POST'])
@login_required
def quiz_tema(tema_id):
    tema = Tema.query.get_or_404(tema_id)
    progreso = ProgresoUsuario.query.filter_by(
        usuario_id=current_user.id, tema_id=tema_id).first_or_404()

    if request.method == 'GET':
        preguntas = PreguntaQuiz.query.filter_by(tema_id=tema_id).all()
        return render_template('student/quiz.html', tema=tema, preguntas=preguntas)

    # POST: calificar el quiz y aplicar la regla de personalización
    preguntas = PreguntaQuiz.query.filter_by(tema_id=tema_id).all()
    correctas = 0
    for pregunta in preguntas:
        respuesta = request.form.get(f'pregunta_{pregunta.id}')
        if respuesta == pregunta.respuesta_correcta:
            correctas += 1

    porcentaje = (correctas / len(preguntas) * 100) if preguntas else 0

    db.session.add(ResultadoQuiz(
        usuario_id=current_user.id, tema_id=tema_id, puntaje=porcentaje))

    # Regla de personalización (RF-06): sube o baja de nivel según umbral
    mensaje_nivel = ''
    era_avanzado = progreso.nivel_actual == 'avanzado'
    if porcentaje >= 80 and progreso.nivel_actual != 'avanzado':
        progreso.nivel_actual = siguiente_nivel(progreso.nivel_actual)
        mensaje_nivel = f' ¡Subiste a nivel {progreso.nivel_actual}!'
    elif porcentaje < 50 and progreso.nivel_actual != 'basico':
        progreso.nivel_actual = nivel_anterior(progreso.nivel_actual)
        mensaje_nivel = f' Bajaste a nivel {progreso.nivel_actual} para reforzar.'

    # Dominado solo si ya estaba en avanzado ANTES de este intento y vuelve a sacar >= 80
    if porcentaje >= 80 and era_avanzado:
        progreso.estado = 'dominado'
        mensaje_nivel = ' ¡Dominaste este tema!'

    db.session.commit()

    flash(f'Obtuviste {porcentaje:.0f}% en el quiz.{mensaje_nivel}', 'success')
    return redirect(url_for('student.ver_tema', tema_id=tema_id))

@student_bp.route('/unirse-salon', methods=['GET', 'POST'])
@login_required
def unirse_salon():
    if request.method == 'POST':
        codigo = request.form.get('codigo', '').strip().upper()
        salon = Salon.query.filter_by(codigo_acceso=codigo).first()

        if salon is None:
            flash('Código de salón inválido.', 'error')
            return redirect(url_for('student.unirse_salon'))

        ya_inscrito = SalonEstudiante.query.filter_by(
            salon_id=salon.id, usuario_id=current_user.id).first()
        if ya_inscrito:
            flash('Ya estás inscrito en ese salón.', 'error')
            return redirect(url_for('student.dashboard'))

        db.session.add(SalonEstudiante(salon_id=salon.id, usuario_id=current_user.id))
        db.session.commit()
        flash(f'Te uniste al salón "{salon.nombre}".', 'success')
        return redirect(url_for('student.dashboard'))

    return render_template('student/unirse_salon.html')