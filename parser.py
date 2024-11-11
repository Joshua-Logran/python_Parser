import ply.lex as lex
import ply.yacc as yacc

flag_lexical_error = False
flag_sintax_error = False
flag_semantic_error = False

result = 0
symbol_table = {}

# General token list
tokens = ('PUNCTUATION', 'OPERATOR', 'LITERAL', 'KEYWORD', 'IDENTIFIER', 'NUMBER', 'INCLUDE', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULUS', 'EXPONENT')

# C keywords, excluding 'main' so it is treated as IDENTIFIER
keywords = {
    'int': 'KEYWORD',
    'return': 'KEYWORD',
    'char': 'KEYWORD',
    'float': 'KEYWORD',
    'double': 'KEYWORD',
    'void': 'KEYWORD',
}

# Regular expressions for each token category
t_PUNCTUATION = r'[;{}()]'
t_OPERATOR = r'='
t_INCLUDE = r'\#include\s+<\w+\.h>'

# Operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULUS = r'%'
t_EXPONENT = r'\^'

# Regular expression for literal strings
def t_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''
    return t

# Identifiers, which could be keywords or variables
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')  # 'main' is not in keywords
    return t

# Numbers
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignore spaces and tabs
t_ignore = ' \t'

# Handle new lines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Handle lexical errors
def t_error(t):
    print(f"Illegal character '{t.value[0]}' on line {t.lineno}")
    t.lexer.skip(1)
    global flag_lexical_error
    flag_lexical_error = True

# Build the lexer
lexer = lex.lex()

# Define grammar for the parser
def p_program(p):
    '''program : INCLUDE function'''
    #print("Valid C program")

def p_function(p):
    '''function : KEYWORD IDENTIFIER PUNCTUATION PUNCTUATION block'''
    #print("Valid function")
    pass

def p_block(p):
    '''block : PUNCTUATION declarations statements return_statement PUNCTUATION '''
    #print("Valid block")
    pass

def p_declarations(p):
    '''declarations : declaration PUNCTUATION
                    | declarations declaration PUNCTUATION'''
    #print("Valid declarations")
    pass

def p_declaration(p):
    '''declaration : KEYWORD IDENTIFIER'''
    #print("Valid declaration")
    var_type = p[1]
    var_name = p[2]
    if var_name in symbol_table:
        print(f"Semantic error: the variable '{var_name}' is already declared.")
        global flag_semantic_error
        flag_semantic_error = True
    else:
        symbol_table[var_name] = var_type
        #print(f"Declaration detected: {var_name} of type {var_type}")

def p_statements(p):
    '''statements : statement PUNCTUATION
                  | statements statement PUNCTUATION
                  '''
    #print("Valid statements")
    pass

def p_operation(p):
    '''operation : NUMBER PLUS NUMBER
                 | NUMBER MINUS NUMBER
                 | NUMBER TIMES NUMBER
                 | NUMBER DIVIDE NUMBER
                 | NUMBER MODULUS NUMBER
                 | NUMBER EXPONENT NUMBER'''
    p[1] = int(p[1])
    p[3] = int(p[3])
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]
    elif p[2] == '^':
        p[0] = p[1] ** p[3]
    #print("Valid arithmetic operation = ", p[0])

def p_statement(p):
    '''statement : assignment_statement
                 | IDENTIFIER PUNCTUATION LITERAL PUNCTUATION
                 | assignment_operation'''
    #print("Valid statement")

def p_assignment_statement(p):
    ''' assignment_statement : IDENTIFIER OPERATOR NUMBER 
                             | IDENTIFIER OPERATOR LITERAL
                             '''
    var_name = p[1]
    global flag_semantic_error
    if var_name not in symbol_table:
        print(f"Semantic error: the variable '{var_name}' has not been declared yet.")
        flag_semantic_error = True
    else:
        var_type = str(symbol_table[var_name])
        expr_type = type(p[3]).__name__  # Type of the expression
        if var_type != expr_type:
            print(f"Semantic error: can't assign a value of type '{expr_type}' to the variable '{var_name}' of type '{var_type}'.")
            flag_semantic_error = True
        #else:
            #print(f"Valid assignment: {var_name} = {p[3]}")
            #print("Valid assignment")

def p_assignment_operation(p):
    '''assignment_operation : IDENTIFIER OPERATOR operation'''
    #print("Value to assign: ", p[3])
    var_name = p[1]
    if var_name not in symbol_table:
        print(f"Semantic error: the variable '{var_name}' has not been declared yet.")
    else:
        var_type = str(symbol_table[var_name])
        expr_type = type(p[3]).__name__  # Type of the expression
        if var_type != expr_type:
            print(f"Semantic error: can't assign a value of type '{expr_type}' to the variable '{var_name}' of type '{var_type}'.")
            global flag_semantic_error
            flag_semantic_error = True
        #else:
            #print(f"Valid assignment: {var_name} = {p[3]}")
        #print("Valid assignment")

def p_return_statement(p):
    '''return_statement : KEYWORD NUMBER PUNCTUATION'''
    #print("Valid return statement")
    pass

# Handle syntactic errors
def p_error(p):
    global flag_sintax_error
    flag_sintax_error = True
    if p:
        print(f"Syntax error in '{p.value}'")
    else:
        print("Syntax error at the end of the file")

# Build the parser
parser = yacc.yacc()

# Sample code to analyze
code = '''
#include <stdio.h>
int main() {
    int a;
    int b;
    printf("Hello, world!");
    a = 5^2;
    b = 3+2;
    return 0;
}
'''

# Pass code to lexer and parser
lexer.input(code)
#print("Generated tokens:")
while True:
    tok = lexer.token()
    if not tok:
        break
    #print(tok)

# Run the parser
if flag_lexical_error:
    print("Lexing error")
else:
    print("Syntactic analysis result:")
    result = parser.parse(code)
    
    if flag_sintax_error and flag_semantic_error:
        print("Parsing error")
        print("SDT error")
    elif not flag_sintax_error and flag_semantic_error:
        print("Parsing success")
        print("SDT error")
    else:
        print("Parsing success")
        print("SDT success")
