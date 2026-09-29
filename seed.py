from app import create_app, db
from app.models import Materia, Tema, PreguntaDiagnostico, Recurso

app = create_app()

with app.app_context():
    # Limpia datos previos de esta materia piloto (útil si vuelves a correr el script)
    materia_existente = Materia.query.filter_by(nombre='Programación en Python').first()
    if materia_existente:
        print('La materia piloto ya existe, no se vuelve a crear.')
    else:
        materia = Materia(
            nombre='Programación en Python',
            descripcion='Fundamentos de programación usando el lenguaje Python.'
        )
        db.session.add(materia)
        db.session.flush()  # para obtener materia.id antes del commit final

        tema1 = Tema(materia_id=materia.id, nombre='Variables y tipos de datos', nivel='basico')
        tema2 = Tema(materia_id=materia.id, nombre='Condicionales y bucles', nivel='basico')
        db.session.add_all([tema1, tema2])
        db.session.flush()

        # --- Preguntas de diagnóstico (varias por tema, se elige una al azar) ---
        preguntas = [
            PreguntaDiagnostico(
                tema_id=tema1.id,
                enunciado='¿Cuál de las siguientes es una forma válida de declarar una variable en Python?',
                opciones=['a) var x = 5', 'b) x = 5', 'c) int x = 5;', 'd) declare x = 5'],
                respuesta_correcta='b'
            ),
            PreguntaDiagnostico(
                tema_id=tema1.id,
                enunciado='¿Qué tipo de dato es el resultado de 5 / 2 en Python 3?',
                opciones=['a) int', 'b) str', 'c) float', 'd) bool'],
                respuesta_correcta='c'
            ),
            PreguntaDiagnostico(
                tema_id=tema1.id,
                enunciado='¿Cuál función se usa para saber el tipo de una variable?',
                opciones=['a) typeof()', 'b) type()', 'c) gettype()', 'd) kind()'],
                respuesta_correcta='b'
            ),
            PreguntaDiagnostico(
                tema_id=tema2.id,
                enunciado='¿Qué palabra clave se usa para un ciclo que repite mientras una condición sea verdadera?',
                opciones=['a) for', 'b) repeat', 'c) while', 'd) loop'],
                respuesta_correcta='c'
            ),
            PreguntaDiagnostico(
                tema_id=tema2.id,
                enunciado='¿Cuál es la sintaxis correcta de un condicional en Python?',
                opciones=['a) if (x > 5) {}', 'b) if x > 5:', 'c) if x > 5 then', 'd) when x > 5:'],
                respuesta_correcta='b'
            ),
            PreguntaDiagnostico(
                tema_id=tema2.id,
                enunciado='¿Qué hace la instrucción "break" dentro de un ciclo?',
                opciones=['a) Reinicia el ciclo', 'b) Salta a la siguiente iteración', 'c) Termina el ciclo por completo', 'd) Pausa el programa'],
                respuesta_correcta='c'
            ),
        ]
        db.session.add_all(preguntas)

        # --- Recursos por nivel (esto es lo que ve el estudiante según su nivel actual) ---
        recursos = [
            Recurso(tema_id=tema1.id, nivel='basico',
                    tipo='lectura',
                    contenido='Una variable es un espacio en memoria para guardar un valor. '
                               'En Python se crea así: x = 5. No es necesario declarar el tipo, '
                               'Python lo detecta automáticamente.'),
            Recurso(tema_id=tema1.id, nivel='intermedio',
                    tipo='lectura',
                    contenido='Python maneja varios tipos: int, float, str, bool, list, dict. '
                               'Puedes verificar el tipo con type(variable), y convertir entre tipos '
                               'con funciones como int(), str(), float().'),
            Recurso(tema_id=tema1.id, nivel='avanzado',
                    tipo='ejercicio',
                    contenido='Reto: escribe una función que reciba una lista de valores mixtos '
                               '(números y strings) y regrese solo los que son numéricos, '
                               'convertidos a float.'),

            Recurso(tema_id=tema2.id, nivel='basico',
                    tipo='lectura',
                    contenido='Un condicional (if/else) ejecuta código solo si se cumple una condición. '
                               'Un ciclo (for/while) repite código varias veces.'),
            Recurso(tema_id=tema2.id, nivel='intermedio',
                    tipo='lectura',
                    contenido='Puedes combinar condicionales con elif para varias opciones, '
                               'y usar continue/break para controlar el flujo dentro de un ciclo.'),
            Recurso(tema_id=tema2.id, nivel='avanzado',
                    tipo='ejercicio',
                    contenido='Reto: escribe un programa que imprima solo los números primos '
                               'entre 1 y 100 usando un ciclo for y condicionales.'),
        ]
        db.session.add_all(recursos)

        db.session.commit()
        print('Materia piloto "Programación en Python" creada con 2 temas, 6 preguntas y 6 recursos.')