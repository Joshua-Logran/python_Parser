import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens generales
"""
tokens = [
    'PUNCTUATION',
    'IDENTIFIER',
    'OPERATOR',
    'LITERAL',
    'KEYWORD',
    'NUMBER',
    'INCLUDE'
]
"""

tokens = ('PUNCTUATION', 'OPERATOR', 'LITERAL', 'KEYWORD', 'IDENTIFIER', 'NUMBER', 'INCLUDE')

# Palabras clave en C, sin incluir 'main' para que sea tratado como IDENTIFIER
keywords = {
    'int': 'KEYWORD',
    'return': 'KEYWORD'
}


# Expresiones regulares para cada categoría de token
t_PUNCTUATION = r'[;{}()]'
t_OPERATOR = r'='
t_INCLUDE = r'\#include\s+<\w+\.h>'

# Expresión regular para cadenas literales
def t_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

# Identificadores, que podrían ser palabras clave o variables
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')  # 'main' no está en keywords
    return t

# Números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de nuevas líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores léxicos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Definir la gramática para el parser
def p_program(p):
    '''program : INCLUDE function'''
    print("Programa C válido")

def p_function(p):
    '''function : KEYWORD IDENTIFIER PUNCTUATION PUNCTUATION block'''
    print("Función válida")
    pass

def p_block(p):
    '''block : PUNCTUATION declarations statements return_statement PUNCTUATION '''
    print("Bloque válido")
    pass

def p_declarations(p):
    '''declarations : declaration
                    | declarations declaration'''
    print("Declaraciones válidas")
    pass

def p_declaration(p):
    '''declaration : KEYWORD IDENTIFIER PUNCTUATION'''
    print("Declaración válida")
    pass

def p_statements(p):
    '''statements : statement PUNCTUATION
                  | statements statement PUNCTUATION'''
    print("Sentencias válidas")
    pass

def p_statement(p):
    '''statement : IDENTIFIER OPERATOR NUMBER
                 | IDENTIFIER PUNCTUATION LITERAL PUNCTUATION'''
    print("Sentencia válida")
    pass

def p_return_statement(p):
    '''return_statement : KEYWORD NUMBER PUNCTUATION'''
    print("Sentencia de retorno válida")
    pass

# Manejo de errores sintácticos
def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}'")
    else:
        print("Error de sintaxis al final del archivo")

# Construir el parser
parser = yacc.yacc()

# Código de ejemplo para analizar
code = '''
#include <stdio.h>
int main() {
    int a;
    a = 5;
    printf("Hola, mundo!\\n");
    return 0;
}
'''

# Pasar el código al lexer y parser
lexer.input(code)
print("Tokens generados:")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

# Ejecutar el parser
print("\nResultado del análisis sintáctico:")
result = parser.parse(code)