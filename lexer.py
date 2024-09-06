import re

# Definición de tokens como expresiones regulares
TOKENS = [
    ('class', r'\bclass\b'),
    ('def', r'\bdef\b'),
    ('if', r'\bif\b'),
    ('else', r'\belse\b'),
    ('while', r'\bwhile\b'),
    ('for', r'\bfor\b'),
    ('print', r'\bprint\b'),
    ('return', r'\breturn\b'),
    ('id', r'[a-zA-Z_][a-zA-Z_0-9]*'),
    ('tk_par_izq', r'\('),
    ('tk_par_der', r'\)'),
    ('tk_llave_izq', r'\{'),
    ('tk_llave_der', r'\}'),
    ('tk_dos_puntos', r':'),
    ('tk_asig', r'='),
    ('tk_mas', r'\+'),
    ('tk_menos', r'-'),
    ('tk_mult', r'\*'),
    ('tk_div', r'/'),
    ('numero', r'\d+'),
    ('tk_punto', r'\.'),
    ('tk_cadena', r'\".*?\"'),
]

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
            match = None
            for token_tipo, token_regex in TOKENS:
                patron = re.compile(token_regex)
                match = patron.match(linea, pos)
                if match:
                    token = match.group(0)
                    print(f"Token encontrado: {token_tipo} -> {token} (línea {num_linea}, posición {pos + 1})")
                    tokens_encontrados.append((token_tipo, token, num_linea, pos + 1))
                    pos = match.end(0)
                    break
            if not match:
                print(f"Ningún token coincide en la posición {pos + 1} de la línea {num_linea}")
                pos += 1

    return tokens_encontrados

def generar_salida(tokens_encontrados, archivo_salida):
    try:
        with open(archivo_salida, 'w') as f:
            for token in tokens_encontrados:
                f.write(f'<{token[0]},{token[1]},{token[2]},{token[3]}>\n')
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
        print("No se encontraron tokens.")
