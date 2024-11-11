import ply.lex as lex
import ply.yacc as yacc

symbol_table = {}
# Lista de tokens generales
tokens = ('PUNCTUATION', 'OPERATOR', 'LITERAL', 'KEYWORD', 'IDENTIFIER', 'NUMBER', 'INCLUDE')

# Palabras clave en C, sin incluir 'main' para que sea tratado como IDENTIFIER
keywords = {
    'int': 'KEYWORD',
    'return': 'KEYWORD',
    'char': 'KEYWORD',
    'float': 'KEYWORD',
    'double': 'KEYWORD',
    'void': 'KEYWORD',
}


# Expresiones regulares para cada categoría de token
t_PUNCTUATION = r'[;{}()]'
t_OPERATOR = r'='
t_INCLUDE = r'\#include\s+<\w+\.h>'

# Expresión regular para cadenas literales
def t_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''
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
    #print("Programa C válido")

def p_function(p):
    '''function : KEYWORD IDENTIFIER PUNCTUATION PUNCTUATION block'''
    #print("Función válida")
    pass

def p_block(p):
    '''block : PUNCTUATION declarations statements return_statement PUNCTUATION '''
    #print("Bloque válido")
    pass

def p_declarations(p):
    '''declarations : declaration PUNCTUATION
                    | declarations declaration PUNCTUATION'''
    #print("Declaraciones válidas")
    pass

def p_declaration(p):
    '''declaration : KEYWORD IDENTIFIER'''
    #print("Declaración válida")
    var_type = p[1]
    var_name = p[2]
    if var_name in symbol_table:
        print(f"Semantic error: the variable '{var_name}' is already declared.")
    else:
        symbol_table[var_name] = var_type
        #print(f"Declaration detected: {var_name} of the type {var_type}")

def p_statements(p):
    '''statements : statement PUNCTUATION
                  | statements statement PUNCTUATION'''
    #print("Sentencias válidas")
    pass

def p_statement(p):
    '''statement : assignment_statement
                 | IDENTIFIER PUNCTUATION LITERAL PUNCTUATION'''
    #print("Sentencia válida")

def p_assignment_statement(p):
    ''' assignment_statement : IDENTIFIER OPERATOR NUMBER 
                             | IDENTIFIER OPERATOR LITERAL'''
    var_name = p[1]
    if var_name not in symbol_table:
        print(f"Semantic error: the variable'{var_name}' has not been declared yet.")
    else:
        var_type = str(symbol_table[var_name])
        expr_type = type(p[3]).__name__  # Tipo de la expresión
        if var_type != expr_type:
            print(f"Semantic error: cant assign a value of type '{expr_type}' to the variable '{var_name}' of type '{var_type}'.")
        else:
            print(f"Valid assignation: {var_name} = {p[3]}")
        #print("Asignación válida")

def p_return_statement(p):
    '''return_statement : KEYWORD NUMBER PUNCTUATION'''
    #print("Sentencia de retorno válida")
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
    int b;
    a = 'h';
    t = 3;
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
    #print(tok)

# Ejecutar el parser
print("\nResultado del análisis sintáctico:")
result = parser.parse(code)