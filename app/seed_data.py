from app import db
from app.models import Materia, Tema, PreguntaDiagnostico, PreguntaQuiz, Recurso

MATERIA = {
    'nombre': 'Programación en Python',
    'descripcion': 'Fundamentos de programación usando el lenguaje Python.',
}

# Cada tema trae: preguntas de diagnóstico, preguntas de quiz y un recurso por nivel.
# Pregunta = (enunciado, [opciones], letra_correcta)
# Recurso  = (nivel, tipo, contenido)
TEMAS = [
    {
        'nombre': 'Variables y tipos de datos',
        'diagnostico': [
            ('¿Cuál de las siguientes es una forma válida de declarar una variable en Python?',
             ['a) var x = 5', 'b) x = 5', 'c) int x = 5;', 'd) declare x = 5'], 'b'),
            ('¿Qué tipo de dato es el resultado de 5 / 2 en Python 3?',
             ['a) int', 'b) str', 'c) float', 'd) bool'], 'c'),
            ('¿Cuál función se usa para saber el tipo de una variable?',
             ['a) typeof()', 'b) type()', 'c) gettype()', 'd) kind()'], 'b'),
        ],
        'quiz': [
            ('¿Qué imprime print(type("10"))?',
             ["a) <class 'int'>", "b) <class 'str'>", "c) <class 'float'>", "d) <class 'bool'>"], 'b'),
            ('¿Cuál es el resultado de int("7") + 3?',
             ['a) 73', 'b) "73"', 'c) 10', 'd) Error'], 'c'),
            ('¿Cuál de estos nombres de variable NO es válido en Python?',
             ['a) mi_edad', 'b) edad2', 'c) 2edad', 'd) _edad'], 'c'),
            ('¿Qué valor tiene x después de: x = 7 // 2 ?',
             ['a) 3.5', 'b) 3', 'c) 4', 'd) 1'], 'b'),
            ('¿Cuál es el tipo de dato de True?',
             ['a) str', 'b) int', 'c) bool', 'd) float'], 'c'),
        ],
        'recursos': [
            ('basico', 'lectura',
             'Una variable es un nombre que guarda un valor en la memoria. En Python se crea con el signo =:\n\n'
             'edad = 18\nnombre = "Ana"\n\n'
             'No hace falta declarar el tipo: Python lo detecta solo. Los tipos más comunes son int (enteros), '
             'float (decimales), str (texto) y bool (verdadero o falso).'),
            ('intermedio', 'lectura',
             'Puedes saber el tipo de una variable con type() y convertir entre tipos con int(), float() y str():\n\n'
             'x = "10"\nprint(type(x))      # <class \'str\'>\nprint(int(x) + 5)   # 15\n\n'
             'Recuerda: 5 / 2 da 2.5 (float), 5 // 2 da 2 (división entera) y 5 % 2 da 1 (residuo).'),
            ('avanzado', 'ejercicio',
             'Reto: escribe una función que reciba una lista de valores mixtos (números y textos) y regrese '
             'solo los que sean numéricos, convertidos a float. Por ejemplo, con [3, "hola", "4.5", 7] '
             'debe regresar [3.0, 4.5, 7.0]. Pista: usa try/except con float().'),
        ],
    },
    {
        'nombre': 'Condicionales y bucles',
        'diagnostico': [
            ('¿Qué palabra clave se usa para un ciclo que repite mientras una condición sea verdadera?',
             ['a) for', 'b) repeat', 'c) while', 'd) loop'], 'c'),
            ('¿Cuál es la sintaxis correcta de un condicional en Python?',
             ['a) if (x > 5) {}', 'b) if x > 5:', 'c) if x > 5 then', 'd) when x > 5:'], 'b'),
            ('¿Qué hace la instrucción "break" dentro de un ciclo?',
             ['a) Reinicia el ciclo', 'b) Salta a la siguiente iteración', 'c) Termina el ciclo por completo', 'd) Pausa el programa'], 'c'),
        ],
        'quiz': [
            ('¿Cuántas veces se imprime "hola"?\n\nfor i in range(3):\n    print("hola")',
             ['a) 2', 'b) 3', 'c) 4', 'd) Infinitas'], 'b'),
            ('¿Qué imprime este código?\n\nx = 10\nif x > 5:\n    print("A")\nelse:\n    print("B")',
             ['a) A', 'b) B', 'c) A y B', 'd) Nada'], 'a'),
            ('¿Qué hace la instrucción "continue" dentro de un ciclo?',
             ['a) Termina el ciclo', 'b) Salta a la siguiente iteración', 'c) Reinicia el programa', 'd) Detiene el programa'], 'b'),
            ('¿Cuál es la palabra clave para una segunda condición en una cadena de condicionales?',
             ['a) elseif', 'b) else if', 'c) elif', 'd) otherwise'], 'c'),
            ('¿Cuál es el último número que imprime range(1, 4)?',
             ['a) 1', 'b) 3', 'c) 4', 'd) 5'], 'b'),
        ],
        'recursos': [
            ('basico', 'lectura',
             'Un condicional ejecuta código solo si se cumple una condición:\n\n'
             'edad = 20\nif edad >= 18:\n    print("Eres mayor de edad")\nelse:\n    print("Eres menor de edad")\n\n'
             'Un ciclo repite código. for recorre una secuencia y while repite mientras la condición sea verdadera. '
             'Fíjate en los dos puntos (:) y en la sangría: Python los usa para saber qué código va dentro.'),
            ('intermedio', 'lectura',
             'Con elif puedes revisar varias opciones, y con break y continue controlas el flujo de un ciclo:\n\n'
             'for n in range(1, 10):\n    if n == 3:\n        continue   # salta el 3\n    if n == 6:\n        break      # termina en el 6\n    print(n)\n\n'
             'Esto imprime 1, 2, 4 y 5.'),
            ('avanzado', 'ejercicio',
             'Reto: escribe un programa que imprima solo los números primos entre 1 y 100, usando un ciclo for '
             'dentro de otro y condicionales. Pista: un número es primo si solo es divisible entre 1 y entre sí mismo.'),
        ],
    },
    {
        'nombre': 'Funciones',
        'diagnostico': [
            ('¿Qué palabra clave se usa para definir una función en Python?',
             ['a) function', 'b) def', 'c) fun', 'd) define'], 'b'),
            ('¿Qué devuelve una función que no tiene instrucción return?',
             ['a) 0', 'b) None', 'c) Una cadena vacía', 'd) False'], 'b'),
            ('En def saludar(nombre="amigo"), ¿qué significa nombre="amigo"?',
             ['a) Que el parámetro es obligatorio', 'b) Que el parámetro tiene un valor por defecto',
              'c) Que la función devuelve "amigo"', 'd) Que es un error de sintaxis'], 'b'),
        ],
        'quiz': [
            ('¿Qué imprime este código?\n\ndef suma(a, b):\n    return a + b\n\nprint(suma(2, 3))',
             ['a) 23', 'b) 5', 'c) None', 'd) Error'], 'b'),
            ('¿Cuál es la diferencia entre parámetro y argumento?',
             ['a) Son exactamente lo mismo',
              'b) El parámetro es la variable en la definición y el argumento es el valor que se envía al llamar',
              'c) El argumento va en la definición y el parámetro al llamar',
              'd) El parámetro solo existe en funciones sin return'], 'b'),
            ('¿Qué pasa cuando se ejecuta un return dentro de una función?',
             ['a) Se sigue ejecutando el resto de la función', 'b) La función termina y devuelve el valor',
              'c) Se reinicia la función', 'd) Se imprime el valor en pantalla'], 'b'),
            ('¿Qué imprime este código?\n\ndef f(x):\n    x = x + 1\n\nn = 5\nf(n)\nprint(n)',
             ['a) 5', 'b) 6', 'c) None', 'd) Error'], 'a'),
            ('¿Qué devuelve f(3)?\n\ndef f(a, b=2):\n    return a * b',
             ['a) 3', 'b) 5', 'c) 6', 'd) Error por faltar b'], 'c'),
        ],
        'recursos': [
            ('basico', 'lectura',
             'Una función es un bloque de código con nombre que puedes reutilizar. Se define con def y se ejecuta al llamarla:\n\n'
             'def saludar(nombre):\n    print("Hola,", nombre)\n\nsaludar("Ana")   # Hola, Ana\n\n'
             'Lo que va entre paréntesis en la definición son los parámetros.'),
            ('intermedio', 'lectura',
             'Una función puede devolver un resultado con return, y sus parámetros pueden tener valores por defecto:\n\n'
             'def area(base, altura=1):\n    return base * altura\n\nprint(area(4, 3))   # 12\nprint(area(4))      # 4\n\n'
             'Si una función no tiene return, devuelve None.'),
            ('avanzado', 'ejercicio',
             'Reto: escribe una función promedio(numeros) que reciba una lista y regrese su promedio. '
             'Si la lista está vacía, debe regresar 0 en lugar de marcar error. '
             'Después escribe otra función que use promedio() para decir si una calificación es aprobatoria (>= 70).'),
        ],
    },
    {
        'nombre': 'Listas y diccionarios',
        'diagnostico': [
            ('Si mi_lista = [10, 20, 30], ¿qué devuelve mi_lista[0]?',
             ['a) 0', 'b) 10', 'c) 20', 'd) Error'], 'b'),
            ('¿Qué método agrega un elemento al final de una lista?',
             ['a) add()', 'b) insert_end()', 'c) append()', 'd) push()'], 'c'),
            ('Dado d = {"nombre": "Ana", "edad": 20}, ¿cómo se obtiene la edad?',
             ['a) d[1]', 'b) d.edad', 'c) d["edad"]', 'd) d(edad)'], 'c'),
        ],
        'quiz': [
            ('¿Qué devuelve len([1, 2, 3, 4])?',
             ['a) 3', 'b) 4', 'c) 5', 'd) 10'], 'b'),
            ('¿Qué imprime este código?\n\nnums = [1, 2, 3]\nnums.append(4)\nprint(nums)',
             ['a) [1, 2, 3]', 'b) [4, 1, 2, 3]', 'c) [1, 2, 3, 4]', 'd) Error'], 'c'),
            ('¿Qué devuelve [10, 20, 30, 40][1:3]?',
             ['a) [10, 20]', 'b) [20, 30]', 'c) [20, 30, 40]', 'd) [10, 20, 30]'], 'b'),
            ('¿Cuál es la diferencia principal entre una lista y un diccionario?',
             ['a) La lista guarda por posición (índice) y el diccionario por clave',
              'b) No hay diferencia', 'c) El diccionario solo guarda números',
              'd) La lista solo guarda texto'], 'a'),
            ('¿Qué imprime este código?\n\nd = {"a": 1}\nd["b"] = 2\nprint(d)',
             ["a) {'a': 1}", "b) {'b': 2}", "c) {'a': 1, 'b': 2}", 'd) Error'], 'c'),
        ],
        'recursos': [
            ('basico', 'lectura',
             'Una lista guarda varios valores en orden. Se crea con corchetes y cada elemento tiene una posición que empieza en 0:\n\n'
             'frutas = ["manzana", "pera", "uva"]\nprint(frutas[0])        # manzana\nfrutas.append("mango")  # agrega al final\n\n'
             'Un diccionario guarda pares clave-valor:\n\n'
             'alumno = {"nombre": "Ana", "edad": 20}\nprint(alumno["nombre"])  # Ana'),
            ('intermedio', 'lectura',
             'Puedes recorrer listas y diccionarios con for, y tomar partes de una lista con rebanadas:\n\n'
             'nums = [10, 20, 30, 40]\nprint(nums[1:3])    # [20, 30]\nprint(nums[-1])     # 40\n\n'
             'alumno = {"nombre": "Ana", "edad": 20}\nfor clave, valor in alumno.items():\n    print(clave, valor)'),
            ('avanzado', 'ejercicio',
             'Reto: dada una lista de diccionarios como [{"nombre": "Ana", "calif": 90}, {"nombre": "Luis", "calif": 60}], '
             'escribe un programa que imprima el nombre de quienes aprobaron (calif >= 70) y el promedio general del grupo.'),
        ],
    },
    {
        'nombre': 'Manejo de errores y archivos',
        'diagnostico': [
            ('¿Qué estructura se usa en Python para capturar errores?',
             ['a) try / except', 'b) catch / throw', 'c) if / error', 'd) check / handle'], 'a'),
            ('¿Qué error ocurre al ejecutar int("hola")?',
             ['a) TypeError', 'b) NameError', 'c) ValueError', 'd) SyntaxError'], 'c'),
            ('¿Qué función se usa para abrir un archivo en Python?',
             ['a) file()', 'b) open()', 'c) read()', 'd) load()'], 'b'),
        ],
        'quiz': [
            ('¿Qué error produce print(10 / 0)?',
             ['a) ValueError', 'b) TypeError', 'c) ZeroDivisionError', 'd) NameError'], 'c'),
            ('¿Para qué sirve with open("datos.txt") as f: ?',
             ['a) Para borrar el archivo', 'b) Para abrir el archivo y cerrarlo automáticamente al terminar',
              'c) Para copiar el archivo', 'd) Para comprobar que el archivo existe'], 'b'),
            ('¿Qué modo se usa para escribir en un archivo borrando su contenido anterior?',
             ['a) "r"', 'b) "a"', 'c) "w"', 'd) "x+"'], 'c'),
            ('¿Qué bloque se ejecuta siempre, haya o no error?',
             ['a) else', 'b) except', 'c) finally', 'd) try'], 'c'),
            ('¿Qué imprime este código?\n\ntry:\n    x = int("5")\nexcept ValueError:\n    print("error")\nelse:\n    print("ok")',
             ['a) error', 'b) ok', 'c) error y ok', 'd) Nada'], 'b'),
        ],
        'recursos': [
            ('basico', 'lectura',
             'Los errores pueden detener tu programa. Con try y except puedes manejarlos sin que el programa se caiga:\n\n'
             'try:\n    numero = int(input("Número: "))\nexcept ValueError:\n    print("Eso no es un número")\n\n'
             'Si el usuario escribe texto en lugar de un número, se ejecuta el except.'),
            ('intermedio', 'lectura',
             'Para leer y escribir archivos usa open() con with, que lo cierra solo:\n\n'
             'with open("notas.txt", "w") as f:\n    f.write("Hola\\n")\n\n'
             'with open("notas.txt", "r") as f:\n    print(f.read())\n\n'
             'Modos comunes: "r" leer, "w" escribir (borra lo anterior) y "a" agregar al final.'),
            ('avanzado', 'ejercicio',
             'Reto: escribe un programa que pida nombres al usuario y los guarde en un archivo, uno por línea. '
             'Después debe leer el archivo y mostrar cuántos nombres hay. Debe manejar el error si el archivo no existe '
             'usando try/except FileNotFoundError.'),
        ],
    },
]


def cargar_datos_ejemplo():
    """Carga (o completa) la materia piloto. Es idempotente: no duplica lo que ya existe."""
    materia = Materia.query.filter_by(nombre=MATERIA['nombre']).first()
    if materia is None:
        materia = Materia(**MATERIA)
        db.session.add(materia)
        db.session.flush()

    for datos in TEMAS:
        tema = Tema.query.filter_by(materia_id=materia.id, nombre=datos['nombre']).first()
        if tema is None:
            tema = Tema(materia_id=materia.id, nombre=datos['nombre'], nivel='basico')
            db.session.add(tema)
            db.session.flush()

        for modelo, clave in ((PreguntaDiagnostico, 'diagnostico'), (PreguntaQuiz, 'quiz')):
            existentes = {p.enunciado for p in modelo.query.filter_by(tema_id=tema.id).all()}
            for enunciado, opciones, correcta in datos[clave]:
                if enunciado not in existentes:
                    db.session.add(modelo(tema_id=tema.id, enunciado=enunciado,
                                          opciones=opciones, respuesta_correcta=correcta))

        for nivel, tipo, contenido in datos['recursos']:
            recurso = Recurso.query.filter_by(tema_id=tema.id, nivel=nivel).first()
            if recurso is None:
                db.session.add(Recurso(tema_id=tema.id, nivel=nivel, tipo=tipo, contenido=contenido))
            else:  # mantiene el contenido actualizado con esta versión
                recurso.tipo = tipo
                recurso.contenido = contenido

    db.session.commit()
