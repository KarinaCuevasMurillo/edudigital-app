"""Datos de demostración: un salón con estudiantes ficticios en distintos estados."""
import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app import db
from app.models import Usuario, Tema, ProgresoUsuario, ResultadoQuiz, SalonEstudiante

DOMINIO_DEMO = '@edudigital.demo'

# (nombre ficticio, puntajes de los quizzes del más antiguo al más reciente, días desde el último, nivel base)
ESTUDIANTES_DEMO = [
    ('Ana Demo',      [60, 75, 90], 1,  'avanzado'),    # avance
    ('Luis Demo',     [70, 85, 95], 2,  'avanzado'),    # avance
    ('Marta Demo',    [55, 60, 65], 3,  'intermedio'),  # estable
    ('Diego Demo',    [50, 70, 60], 5,  'intermedio'),  # estable
    ('Sofía Demo',    [70, 50, 30], 2,  'basico'),      # decadencia (puntaje bajo)
    ('Pablo Demo',    [80, 70, 65], 20, 'intermedio'),  # decadencia (inactividad)
    ('Elena Demo',    [],           0,  'basico'),      # sin actividad
    ('Raúl Demo',     [],           0,  'basico'),      # sin actividad
]


def es_usuario_demo(usuario):
    return usuario.correo.endswith(DOMINIO_DEMO)


def crear_estudiantes_demo(salon):
    """Crea los estudiantes ficticios, su progreso y sus quizzes, y los inscribe en el salón."""
    temas = Tema.query.order_by(Tema.id).all()
    ahora = datetime.utcnow()

    for i, (nombre, puntajes, dias, nivel) in enumerate(ESTUDIANTES_DEMO, start=1):
        usuario = Usuario(
            nombre=nombre,
            correo=f'demo{i}.salon{salon.id}{DOMINIO_DEMO}',
            # contraseña aleatoria que nadie conoce: estas cuentas no pueden iniciar sesión
            contrasena_hash=generate_password_hash(secrets.token_hex(16)),
            rol='estudiante',
        )
        db.session.add(usuario)
        db.session.flush()

        db.session.add(SalonEstudiante(salon_id=salon.id, usuario_id=usuario.id))

        if puntajes:
            for tema in temas:
                db.session.add(ProgresoUsuario(usuario_id=usuario.id, tema_id=tema.id,
                                               nivel_actual=nivel, estado='en_curso'))
            tema_quiz = temas[0] if temas else None
            for j, puntaje in enumerate(puntajes):
                if tema_quiz is None:
                    break
                dias_atras = dias + (len(puntajes) - 1 - j) * 3
                db.session.add(ResultadoQuiz(usuario_id=usuario.id, tema_id=tema_quiz.id,
                                             puntaje=puntaje, fecha=ahora - timedelta(days=dias_atras)))


def borrar_usuarios_demo(usuarios):
    """Elimina por completo a los estudiantes ficticios (y su progreso) de un salón que se borra."""
    for usuario in usuarios:
        if es_usuario_demo(usuario):
            ResultadoQuiz.query.filter_by(usuario_id=usuario.id).delete()
            ProgresoUsuario.query.filter_by(usuario_id=usuario.id).delete()
            db.session.delete(usuario)
