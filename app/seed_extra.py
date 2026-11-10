# Preguntas adicionales para el uso con un salón real.
# En cada pregunta la opción correcta se escribe PRIMERO (sin letra); después
# app/seed_data.py las reparte entre a, b, c y d para que no haya una letra favorita.
# Pregunta = (enunciado, [opcion_correcta, otra, otra, otra])

EXTRA = {
    'Variables y tipos de datos': {
        'diagnostico': [
            ('¿Qué imprime print(type(3.0))?',
             ["<class 'float'>", "<class 'int'>", "<class 'str'>", "<class 'number'>"]),
            ('¿Cuál de estos valores es de tipo str?',
             ['"25"', '25', '25.0', 'True']),
        ],
        'quiz': [
            ('¿Qué valor tiene x después de: x = 10 % 3 ?',
             ['1', '3', '0', '3.33']),
            ('¿Qué imprime print("5" + "3")?',
             ['53', '8', 'Error', '5 3']),
            ('¿Qué hace float("2.5")?',
             ['Convierte el texto "2.5" en el número decimal 2.5',
              'Marca un error porque tiene punto',
              'Regresa el entero 2',
              'Regresa el mismo texto sin cambios']),
            ('¿Cuál es el resultado de 2 ** 3 ?',
             ['8', '6', '9', '5']),
        ],
    },
    'Condicionales y bucles': {
        'diagnostico': [
            ('¿Cuántas veces se ejecuta el cuerpo de un ciclo for i in range(3): ?',
             ['3 veces', '2 veces', '4 veces', 'Infinitas veces']),
            ('¿Qué operador se usa para comprobar si dos valores son iguales?',
             ['==', '=', '===', 'equals']),
        ],
        'quiz': [
            ('¿Qué imprime este código?\n\nfor i in range(1, 4):\n    print(i)',
             ['1, 2 y 3, cada número en su línea', '0, 1, 2 y 3', '1, 2, 3 y 4', 'Solo 1 y 2']),
            ('¿Qué hace la instrucción "continue" dentro de un ciclo?',
             ['Salta a la siguiente iteración', 'Termina el ciclo', 'Reinicia el programa', 'No hace nada']),
            ('¿Qué imprime este código?\n\nx = 8\nif x > 10:\n    print("A")\nelif x > 5:\n    print("B")\nelse:\n    print("C")',
             ['B', 'A', 'C', 'B y C']),
            ('¿Qué imprime este código?\n\nn = 0\nwhile n < 3:\n    n += 1\nprint(n)',
             ['3', '0', '2', 'Nada']),
        ],
    },
    'Funciones': {
        'diagnostico': [
            ('¿Qué palabra clave se usa para definir una función en Python?',
             ['def', 'function', 'func', 'define']),
            ('¿Qué devuelve una función que no tiene la instrucción return?',
             ['None', '0', 'Un error', 'Una cadena vacía']),
        ],
        'quiz': [
            ('¿Qué imprime este código?\n\ndef doble(x):\n    return x * 2\n\nprint(doble(4))',
             ['8', '4', '6', 'doble(4)']),
            ('¿Qué es un parámetro de una función?',
             ['Una variable que aparece en la definición y recibe un valor al llamarla',
              'El resultado que regresa la función',
              'El nombre del archivo donde está la función',
              'Un tipo de error']),
            ('¿Qué imprime este código?\n\ndef saludo(nombre="amigo"):\n    return "Hola " + nombre\n\nprint(saludo())',
             ['Hola amigo', 'Hola', 'Error', 'Hola nombre']),
            ('¿Cuál es la diferencia entre print() y return?',
             ['return entrega un valor a quien llamó la función; print solo lo muestra en pantalla',
              'Son exactamente lo mismo',
              'print entrega un valor y return lo muestra en pantalla',
              'return solo funciona con números']),
        ],
    },
    'Listas y diccionarios': {
        'diagnostico': [
            ('¿Qué devuelve len([1, 2, 3])?',
             ['3', '2', '4', '1']),
            ('Dado d = {"edad": 20}, ¿cómo se obtiene el valor 20?',
             ['d["edad"]', 'd[0]', 'd.edad', 'd(edad)']),
        ],
        'quiz': [
            ('¿Qué imprime este código?\n\nnums = [1, 2, 3]\nnums.append(4)\nprint(len(nums))',
             ['4', '3', '5', '[1, 2, 3, 4]']),
            ('¿Qué imprime print(["a", "b", "c"][1])?',
             ['b', 'a', 'c', 'Error']),
            ('Dado d = {"a": 1}, ¿qué regresa d.get("x")?',
             ['None', 'Error', '0', '"x"']),
            ('¿Qué imprime este código?\n\nnums = [5, 3, 8]\nnums.sort()\nprint(nums)',
             ['[3, 5, 8]', '[5, 3, 8]', '[8, 5, 3]', 'None']),
        ],
    },
    'Manejo de errores y archivos': {
        'diagnostico': [
            ('¿Qué error aparece al usar una variable que no se ha definido?',
             ['NameError', 'ValueError', 'TypeError', 'IndexError']),
            ('¿Qué modo se usa para abrir un archivo solo para leerlo?',
             ['"r"', '"w"', '"a"', '"x"']),
        ],
        'quiz': [
            ('¿Qué bloque se usa para capturar un error?',
             ['except', 'finally', 'else', 'raise']),
            ('¿Qué error se produce al abrir con open() un archivo que no existe?',
             ['FileNotFoundError', 'ValueError', 'NameError', 'ZeroDivisionError']),
            ('¿Qué regresa el método f.readlines() de un archivo abierto?',
             ['Una lista con cada línea del archivo', 'Solo la primera línea',
              'Un número con la cantidad de líneas', 'Todo el archivo como un número']),
            ('¿Qué instrucción lanza un error a propósito?',
             ['raise', 'throw', 'error', 'except']),
        ],
    },
}
