import os;

TOKENS = {
    'class': 'class',
    'def': 'def',
    'if': 'if',
    'else': 'else',
    'while': 'while',
    'for': 'for',
    'in': 'in',
    'range': 'range',
    'False': 'False',
    'None': 'None',
    'True': 'True',
    'and': 'and',
    'as': 'as',
    'assert': 'assert',
    'async': 'async',
    'await': 'await',
    'break': 'break',
    'class': 'class',
    'continue': 'continue',
    'def': 'def',
    'del': 'del',
    'elif': 'elif',
    'else': 'else',
    'except': 'except',
    'finally': 'finally',
    'for': 'for',
    'from': 'from',
    'global': 'global',
    'if': 'if',
    'import': 'import',
    'in': 'in',
    'is': 'is',
    'lambda': 'lambda',
    'nonlocal': 'nonlocal',
    'not': 'not',
    'or': 'or',
    'pass': 'pass',
    'raise': 'raise',
    'return': 'return',
    'try': 'try',
    'while': 'while',
    'with': 'with',
    'yield': 'yield',
    'print': 'print',
    'tk_par_izq': '(',
    'tk_par_der': ')',
    'tk_llave_izq': '{',
    'tk_llave_der': '}',
    'tk_cor_izq': '[',
    'tk_cor_der': ']',
    'tk_dos_puntos': ':',
    'tk_asig': '=',
    'tk_mas': '+',
    'tk_menos': '-',
    'tk_mult': '*',
    'tk_div': '/',
    'tk_punto': '.',
    'tk_mayor': '>',
    'tk_menor': '<',
    'tk_flecha': '->',
    'tk_coma': ',',
    'tk_punto_coma': ';',
    'tk_igual_igual': '==',
    'tk_distinto': '!=',
    'tk_mayor_igual': '>=',
    'tk_menor_igual': '<=',
}

def es_digito(c):
    return '0' <= c <= '9'

def es_letra(c):
    return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_'

def es_espacio(c):
    return c in [' ', '\t', '\n']

def es_operador(c):
    return c in ['+', '-', '*', '/', '=', '>', '<']

def es_separador(c):
    return c in ['(', ')', '{', '}', '[', ']', ':', '.', ',', ';']

def es_comentario(linea, pos):
    return linea[pos] == '#'

def leer_palabra(linea, pos):
    palabra = ''
    while pos < len(linea) and (es_letra(linea[pos]) or es_digito(linea[pos])):
        palabra += linea[pos]
        pos += 1
    return palabra, pos

def leer_numero(linea, pos):
    numero = ''
    punto_visto = False
    while pos < len(linea) and (es_digito(linea[pos]) or (linea[pos] == '.' and not punto_visto)):
        if linea[pos] == '.':
            punto_visto = True
        numero += linea[pos]
        pos += 1
    return numero, pos

def leer_string(linea, pos):
    cadena = ''
    delimitador = linea[pos]  # Puede ser ' o "
    pos += 1

    while pos < len(linea) and linea[pos] != delimitador:
        cadena += linea[pos]
        pos += 1

    return delimitador + cadena + delimitador, pos + 1  # Regresar el string con las comillas

def imprimir_error_lexico(linea, num_linea, pos):
    print(f">>> Error léxico (línea:{num_linea}, posición:{pos + 1})")

def analizador_lexico(archivo_entrada):
    try:
        with open(archivo_entrada, 'r') as f:
            codigo = f.read()
            print(f"Archivo de entrada leído correctamente: {archivo_entrada}")
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_entrada}' no existe.")
        return [], []

    tokens_encontrados = []
    errores_lexicos = []
    lineas = codigo.split('\n')

    for num_linea, linea in enumerate(lineas, 1):
        pos = 0
        print(f"Analizando línea {num_linea}: {linea}")
        while pos < len(linea):
            if es_espacio(linea[pos]):
                pos += 1
                continue

            if es_comentario(linea, pos):
                break

            token = None

            if pos + 1 < len(linea) and linea[pos:pos+2] in TOKENS.values():
                # Verificar si el símbolo de 2 caracteres está en TOKENS
                for key, value in TOKENS.items():
                    if value == linea[pos:pos+2]:
                        token = (key, num_linea, pos + 1)  # Obtenemos el nombre del token
                        break
                pos += 2

            elif es_letra(linea[pos]):
                palabra, nuevo_pos = leer_palabra(linea, pos)
                if palabra in TOKENS:
                    token = (palabra, num_linea, pos + 1)  # Solo el nombre del token
                else:
                    token = ('id', palabra, num_linea, pos + 1)
                pos = nuevo_pos

            elif es_digito(linea[pos]) or (linea[pos] == '.' and pos + 1 < len(linea) and es_digito(linea[pos + 1])):
                numero, nuevo_pos = leer_numero(linea, pos)
                token_tipo = 'tk_flotante' if '.' in numero else 'tk_entero'
                token = (token_tipo, numero, num_linea, pos + 1)
                pos = nuevo_pos

            elif linea[pos] in ['"', "'"]:
                cadena, nuevo_pos = leer_string(linea, pos)
                token_tipo = 'tk_cadena_doble' if linea[pos] == '"' else 'tk_cadena_simple'
                token = (token_tipo, cadena, num_linea, pos + 1)
                pos = nuevo_pos

            elif linea[pos] in TOKENS.values():
                # Para un solo carácter
                for key, value in TOKENS.items():
                    if value == linea[pos]:
                        token = (key, num_linea, pos + 1)  # Obtenemos el nombre del token
                        break
                pos += 1

            if token:
                print(f"Token encontrado: {token[0]} (línea {num_linea}, posición {token[2]})")
                tokens_encontrados.append(token)
            else:
                imprimir_error_lexico(linea, num_linea, pos)
                errores_lexicos.append((num_linea, pos + 1))
                pos += 1  # Avanzar para continuar analizando el resto de la línea

    return tokens_encontrados, errores_lexicos

def generar_salida(tokens_encontrados, errores_lexicos, archivo_salida):
    print(f"Generando archivo de salida: {archivo_salida}")
    # Eliminar el archivo de salida si ya existe
    if os.path.exists(archivo_salida):
        print(f"Eliminando el archivo existente: {archivo_salida}")

    try:
        with open(archivo_salida, 'w') as f:
            f.write(f'   ')

            print(f"Generando archivo de salida: {archivo_salida}")

            contenido_generado = False

            # Escribir tokens
            if tokens_encontrados:
                for token in tokens_encontrados:
                    if len(token) == 4:
                        # Este formato es para los tokens con un valor adicional (por ejemplo, identificadores y literales)
                        f.write(f'<{token[0]},{token[1]},{token[2]},{token[3]}>\n')
                    else:
                        # Este formato es para los tokens que no tienen un valor asociado (palabras reservadas y operadores)
                        f.write(f'<{token[0]},{token[1]},{token[2]}>\n')
                contenido_generado = True

            # Escribir errores léxicos
            if errores_lexicos:
                for error in errores_lexicos:
                    f.write(f">>> Error léxico (línea:{error[0]}, posición:{error[1]})\n")
                contenido_generado = True

            # Escribir un mensaje si el archivo está vacío
            if not contenido_generado:
                print("No se encontraron tokens ni errores léxicos.\n")

        print(f"Archivo de salida generado correctamente: {archivo_salida}")
    except Exception as e:
        print(f"Error al escribir en el archivo '{archivo_salida}': {e}")

if __name__ == '__main__':
    archivo_entrada = 'entrada.py'
    archivo_salida = 'salida.txt'

    print(f"Analizando archivo de entrada: {archivo_entrada}")

    tokens, errores_lexicos = analizador_lexico(archivo_entrada)

    generar_salida(tokens, errores_lexicos, archivo_salida)

