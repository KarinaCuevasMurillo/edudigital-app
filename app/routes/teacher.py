import csv
import io
import random
import string
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, Response
from flask_login import login_required, current_user
from app import db
from app.models import (Salon, SalonEstudiante, ResultadoQuiz, ProgresoUsuario, Tema,
                        ResultadoDiagnostico, EncuestaUso)
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


def resumen_estudiante(usuario):
    """Métricas de un estudiante: diagnóstico inicial, quizzes, mejora y encuesta."""
    diag = (ResultadoDiagnostico.query.filter_by(usuario_id=usuario.id)
            .order_by(ResultadoDiagnostico.fecha.asc()).first())
    resultados = (ResultadoQuiz.query.filter_by(usuario_id=usuario.id)
                  .order_by(ResultadoQuiz.fecha.asc()).all())
    prom_quiz = sum(r.puntaje for r in resultados) / len(resultados) if resultados else None

    # Mejora dentro de cada tema: último intento menos primer intento (solo temas con 2 o más intentos)
    por_tema = {}
    for r in resultados:
        por_tema.setdefault(r.tema_id, []).append(r.puntaje)
    mejoras = [v[-1] - v[0] for v in por_tema.values() if len(v) >= 2]
    mejora_intentos = sum(mejoras) / len(mejoras) if mejoras else None

    progresos = ProgresoUsuario.query.filter_by(usuario_id=usuario.id).all()
    dias_sin_actividad = (datetime.utcnow() - resultados[-1].fecha).days if resultados else None

    return {
        'usuario': usuario,
        'diag_pct': diag.porcentaje if diag else None,
        'nivel_inicial': diag.nivel_asignado if diag else None,
        'n_quizzes': len(resultados),
        'prom_quiz': prom_quiz,
        'ultimo_quiz': resultados[-1].puntaje if resultados else None,
        'mejora_vs_diag': (prom_quiz - diag.porcentaje) if (diag and prom_quiz is not None) else None,
        'mejora_intentos': mejora_intentos,
        'temas_dominados': sum(1 for p in progresos if p.estado == 'dominado'),
        'dias_sin_actividad': dias_sin_actividad,
        'estado': estado_estudiante(usuario.id),
        'encuesta': EncuestaUso.query.filter_by(usuario_id=usuario.id).first(),
    }


def _promedio(valores):
    valores = [v for v in valores if v is not None]
    return sum(valores) / len(valores) if valores else None


def _salon_propio(salon_id):
    _solo_docentes()
    salon = Salon.query.get_or_404(salon_id)
    if salon.docente_id != current_user.id:
        abort(403)
    return salon


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

    resumenes = [resumen_estudiante(i['usuario']) for i in estudiantes_info]
    grupo = {
        'prom_diag': _promedio([r['diag_pct'] for r in resumenes]),
        'prom_quiz': _promedio([r['prom_quiz'] for r in resumenes]),
        'mejora_intentos': _promedio([r['mejora_intentos'] for r in resumenes]),
        'con_diag': sum(1 for r in resumenes if r['diag_pct'] is not None),
        'con_quiz': sum(1 for r in resumenes if r['n_quizzes'] > 0),
        'con_encuesta': sum(1 for r in resumenes if r['encuesta'] is not None),
        'mejoraron': sum(1 for r in resumenes if r['mejora_vs_diag'] is not None and r['mejora_vs_diag'] > 0),
        'comparables': sum(1 for r in resumenes if r['mejora_vs_diag'] is not None),
    }
    encuestas = [r['encuesta'] for r in resumenes if r['encuesta'] is not None]
    medias = {c: _promedio([getattr(e, c) for e in encuestas])
              for c in ('facilidad', 'claridad', 'utilidad', 'motivacion', 'recomendaria')}

    return render_template('teacher/salon_detalle.html', salon=salon,
                            estudiantes_info=estudiantes_info, conteo=conteo, promedio=promedio,
                            grupo=grupo, medias=medias)


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
                            resultados=resultados, promedio=promedio,
                            resumen=resumen_estudiante(estudiante))


def _csv_respuesta(nombre_archivo, encabezados, filas):
    salida = io.StringIO()
    escritor = csv.writer(salida)
    escritor.writerow(encabezados)
    escritor.writerows(filas)
    # utf-8-sig para que Excel muestre bien los acentos
    return Response('\ufeff' + salida.getvalue(), mimetype='text/csv; charset=utf-8',
                    headers={'Content-Disposition': f'attachment; filename={nombre_archivo}'})


def _fmt(valor, decimales=1):
    return '' if valor is None else round(valor, decimales)


@teacher_bp.route('/salon/<int:salon_id>/exportar/estudiantes.csv')
@login_required
def exportar_estudiantes(salon_id):
    salon = _salon_propio(salon_id)
    inscripciones = (SalonEstudiante.query.filter_by(salon_id=salon.id)
                     .order_by(SalonEstudiante.fecha_ingreso.asc()).all())
    filas = []
    for n, ins in enumerate(inscripciones, start=1):
        r = resumen_estudiante(ins.estudiante)
        e = r['encuesta']
        filas.append([
            f'E{n:02d}', ins.estudiante.nombre, ins.estudiante.correo,
            ins.estudiante.fecha_registro.strftime('%Y-%m-%d'),
            _fmt(r['diag_pct']), r['nivel_inicial'] or '',
            r['n_quizzes'], _fmt(r['prom_quiz']), _fmt(r['ultimo_quiz']),
            _fmt(r['mejora_vs_diag']), _fmt(r['mejora_intentos']),
            r['temas_dominados'], r['estado'],
            '' if r['dias_sin_actividad'] is None else r['dias_sin_actividad'],
            e.facilidad if e else '', e.claridad if e else '', e.utilidad if e else '',
            e.motivacion if e else '', e.recomendaria if e else '',
            (e.comentario or '') if e else '',
        ])
    return _csv_respuesta('edudigital_estudiantes.csv', [
        'id', 'nombre', 'correo', 'fecha_registro', 'diagnostico_pct', 'nivel_inicial',
        'quizzes_realizados', 'promedio_quiz_pct', 'ultimo_quiz_pct',
        'diferencia_quiz_vs_diagnostico', 'mejora_promedio_entre_intentos',
        'temas_dominados', 'estado', 'dias_sin_actividad',
        'enc_facilidad', 'enc_claridad', 'enc_utilidad', 'enc_motivacion', 'enc_recomendaria',
        'enc_comentario'], filas)


@teacher_bp.route('/salon/<int:salon_id>/exportar/quizzes.csv')
@login_required
def exportar_quizzes(salon_id):
    salon = _salon_propio(salon_id)
    inscripciones = (SalonEstudiante.query.filter_by(salon_id=salon.id)
                     .order_by(SalonEstudiante.fecha_ingreso.asc()).all())
    filas = []
    for n, ins in enumerate(inscripciones, start=1):
        resultados = (ResultadoQuiz.query.filter_by(usuario_id=ins.usuario_id)
                      .order_by(ResultadoQuiz.fecha.asc()).all())
        for r in resultados:
            filas.append([f'E{n:02d}', r.tema.nombre, round(r.puntaje, 1),
                          r.fecha.strftime('%Y-%m-%d %H:%M')])
    return _csv_respuesta('edudigital_quizzes.csv', ['id', 'tema', 'puntaje_pct', 'fecha'], filas)
