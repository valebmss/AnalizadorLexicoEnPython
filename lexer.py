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
    'return': 'return',
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
    'tk_diferente': '!=',
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
    while pos < len(linea) and es_digito(linea[pos]):
        numero += linea[pos]
        pos += 1
    return numero, pos

def leer_string(linea, pos):
    cadena = ''
    delimitador = linea[pos]  # Puede ser ' o "
    pos += 1
    inicio_pos = pos  # Posición inicial para el valor del string sin comillas

    while pos < len(linea) and linea[pos] != delimitador:
        cadena += linea[pos]
        pos += 1

    return delimitador + cadena + delimitador, pos + 1  # Regresar el string con las comillas


def analizador_lexico(archivo_entrada):
    try:
        with open(archivo_entrada, 'r') as f:
            codigo = f.read()
            print(f"Archivo de entrada leído correctamente: {archivo_entrada}")
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_entrada}' no existe.")
        return []

    tokens_encontrados = []
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

            if es_letra(linea[pos]):
                palabra, nuevo_pos = leer_palabra(linea, pos)
                if palabra in TOKENS:
                    token = (palabra, num_linea, pos + 1)  # Solo el nombre del token
                else:
                    token = ('id', palabra, num_linea, pos + 1)
                pos = nuevo_pos

            elif es_digito(linea[pos]):
                numero, nuevo_pos = leer_numero(linea, pos)
                token = ('tk_entero', numero, num_linea, pos + 1)
                pos = nuevo_pos

            elif linea[pos] in ['"', "'"]:
                cadena, nuevo_pos = leer_string(linea, pos)
                token_tipo = 'tk_cadena_doble' if linea[pos] == '"' else 'tk_cadena_simple'
                token = (token_tipo, cadena, num_linea, pos + 1)
                pos = nuevo_pos

            elif es_operador(linea[pos]) or es_separador(linea[pos]):
                # Primero revisamos si el símbolo completo de 2 caracteres está en TOKENS
                if linea[pos:pos+2] in TOKENS.values():
                    for key, value in TOKENS.items():
                        if value == linea[pos:pos+2]:
                            token = (key, num_linea, pos + 1)  # Obtenemos el nombre del token
                            break
                    pos += 2
                else:
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
                print(f">>> Error léxico (línea:{num_linea}, posición:{pos + 1})")
                return []

    return tokens_encontrados

def generar_salida(tokens_encontrados, archivo_salida):
    try:
        with open(archivo_salida, 'w') as f:
            for token in tokens_encontrados:
                if len(token) == 4:
                    # Este formato es para los tokens con un valor adicional (por ejemplo, identificadores y literales)
                    f.write(f'<{token[0]},{token[1]},{token[2]},{token[3]}>\n')
                else:
                    # Este formato es para los tokens que no tienen un valor asociado (palabras reservadas y operadores)
                    f.write(f'<{token[0]},{token[1]},{token[2]}>\n')
        print(f"Archivo de salida generado correctamente: {archivo_salida}")
    except Exception as e:
        print(f"Error al escribir en el archivo '{archivo_salida}': {e}")

if __name__ == '__main__':
    archivo_entrada = 'entrada.py'
    archivo_salida = 'salida.txt'

    print(f"Analizando archivo de entrada: {archivo_entrada}")

    tokens = analizador_lexico(archivo_entrada)
    if tokens:
        print("Tokens encontrados:")
        generar_salida(tokens, archivo_salida)
    else:
        print("No se encontraron tokens o se produjo un error léxico.")
