import ply.lex as lex
import ply.yacc as yacc
# Symbol table for storing variables and types
symbol_table = {}

#Define the tokens
tokens = ('KEYWORD', 'IDENTIFIER', 'CONSTANT', 'OPERATOR', 'LITERAL', 'PUNCTUATION', 'SPECIAL_CHARACTERS', 'SPACE', 'NEWLINE', 'COMMENT', 'OTHER')
t_KEYWORD = r'auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|printf|include'
t_IDENTIFIER = r'[a-zA-Z_$][a-zA-Z_$0-9]*'
t_OTHER = r'\s*<[^>]*>|\<.*?\>'
t_OPERATOR = r'\+|\-|\*|\/|\%|\=\=|\!\=|\>|\>\=|\<|\<\=|\&\&|\|\||\=|\<\<|\>\>|\<\<\=|\>\>\=|\?|\:'
t_COMMENT = r'\/\/.*'
t_CONSTANT = r'\b[0-9]+\b|\d+'
t_LITERAL = r'\".*?\"|\'.\''
t_PUNCTUATION = r'\;|\,|\:|\[|\]|\(|\)|\{|\}'
t_SPECIAL_CHARACTERS = r'\°|\#|\&'

t_ignore = ' \t\n'

# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Syntax Analysis (Parsing)
    # Precedence and associativity of operators
precedence = (
    ('left', 'OPERATOR')
)

# Define the grammar rules
# Rule for declaring variables
def p_statement_declare(p):
    'statement : KEYWORD IDENTIFIER PUNCTUATION'
    var_type = p[1]
    var_name = p[2]
    if var_name in symbol_table:
        print(f"Error semántico: La variable '{var_name}' ya está declarada.")
    else:
        symbol_table[var_name] = var_type
        print(f"Declaración detectada: {var_name} de tipo {var_type}")

# Rule for assigning values to variables
def p_statement_assign(p):
    'statement : IDENTIFIER OPERATOR expression SEMICOLON'
    var_name = p[1]
    if var_name not in symbol_table:
        print(f"Error semántico: La variable '{var_name}' no ha sido declarada.")
    else:
        var_type = symbol_table[var_name]
        expr_type = p[3][1]  # Tipo de la expresión
        if var_type != expr_type:
            print(f"Error semántico: No se puede asignar un valor de tipo '{expr_type}' a la variable '{var_name}' de tipo '{var_type}'.")
        else:
            print(f"Asignación válida: {var_name} = {p[3][0]}")
