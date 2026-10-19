from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='estudiante')  # 'estudiante' o 'docente'
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    progresos = db.relationship('ProgresoUsuario', backref='usuario', lazy=True)
    resultados = db.relationship('ResultadoQuiz', backref='usuario', lazy=True)


class Materia(db.Model):
    __tablename__ = 'materias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)

    temas = db.relationship('Tema', backref='materia', lazy=True)


class Tema(db.Model):
    __tablename__ = 'temas'

    id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    nivel = db.Column(db.String(20), nullable=False)  # 'basico', 'intermedio', 'avanzado'

    preguntas = db.relationship('PreguntaDiagnostico', backref='tema', lazy=True)
    recursos = db.relationship('Recurso', backref='tema', lazy=True)
    progresos = db.relationship('ProgresoUsuario', backref='tema', lazy=True)
    resultados_quiz = db.relationship('ResultadoQuiz', backref='tema', lazy=True)


class PreguntaDiagnostico(db.Model):
    __tablename__ = 'preguntas_diagnostico'

    id = db.Column(db.Integer, primary_key=True)
    tema_id = db.Column(db.Integer, db.ForeignKey('temas.id'), nullable=False)
    enunciado = db.Column(db.Text, nullable=False)
    opciones = db.Column(db.JSON, nullable=False)         # ej: ["a) ...", "b) ...", "c) ...", "d) ..."]
    respuesta_correcta = db.Column(db.String(1), nullable=False)  # 'a', 'b', 'c' o 'd'


class PreguntaQuiz(db.Model):
    """Banco de preguntas del quiz de cada tema (distinto al del diagnóstico)."""
    __tablename__ = 'preguntas_quiz'

    id = db.Column(db.Integer, primary_key=True)
    tema_id = db.Column(db.Integer, db.ForeignKey('temas.id'), nullable=False)
    enunciado = db.Column(db.Text, nullable=False)
    opciones = db.Column(db.JSON, nullable=False)
    respuesta_correcta = db.Column(db.String(1), nullable=False)

    tema = db.relationship('Tema', backref='preguntas_quiz')


class Recurso(db.Model):
    __tablename__ = 'recursos'

    id = db.Column(db.Integer, primary_key=True)
    tema_id = db.Column(db.Integer, db.ForeignKey('temas.id'), nullable=False)
    nivel = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'lectura', 'video', 'ejercicio'
    contenido = db.Column(db.Text, nullable=False)


class ResultadoQuiz(db.Model):
    __tablename__ = 'resultados_quiz'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tema_id = db.Column(db.Integer, db.ForeignKey('temas.id'), nullable=False)
    puntaje = db.Column(db.Float, nullable=False)  # porcentaje 0-100
    fecha = db.Column(db.DateTime, default=datetime.utcnow)


class ProgresoUsuario(db.Model):
    __tablename__ = 'progreso_usuario'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tema_id = db.Column(db.Integer, db.ForeignKey('temas.id'), nullable=False)
    nivel_actual = db.Column(db.String(20), nullable=False, default='basico')
    estado = db.Column(db.String(20), nullable=False, default='en_curso')  # 'en_curso', 'dominado', 'pendiente'


class Salon(db.Model):
    __tablename__ = 'salones'

    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    codigo_acceso = db.Column(db.String(8), unique=True, nullable=False)

    docente = db.relationship('Usuario', foreign_keys=[docente_id])
    estudiantes = db.relationship('SalonEstudiante', backref='salon', lazy=True)


class SalonEstudiante(db.Model):
    __tablename__ = 'salon_estudiante'

    id = db.Column(db.Integer, primary_key=True)
    salon_id = db.Column(db.Integer, db.ForeignKey('salones.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, default=datetime.utcnow)

    estudiante = db.relationship('Usuario', foreign_keys=[usuario_id])