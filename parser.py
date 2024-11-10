import ply.lex as lex
import ply.yacc as yacc

# Symbol table for storing variables and types
symbol_table = {}

# Define the tokens
tokens = (
    'LPAREN', 'RPAREN', 'KEYWORD', 'IDENTIFIER', 'NUMBER',
    'OPERATOR', 'PUNCTUATION', 'INCLUDE', 'HEADER', 'STRING'
)

# Token definitions
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_KEYWORD = r'int|void|return|printf|auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|printf|include'
t_IDENTIFIER = r'[a-zA-Z_$][a-zA-Z_$0-9]*'
t_OPERATOR = r'\=|\=\=|\!\=|\>|\>\=|\<|\<\=|\&\&|\|\||\<\<|\>\>|\<\<\=|\>\>\=|\?|\:'
t_PUNCTUATION = r';|,|\{|\}'  # Covers { and }
t_INCLUDE = r'\#include'
t_HEADER = r'\s*<[^>]*>|\<.*?\>'  # For headers like <stdio.h>
t_STRING = r'\"([^\\"]|\\.)*\"'  # Capture strings, including escaped characters

# Ignored characters (whitespace)
t_ignore = ' \t'

# Define a rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Number token with integer values
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules
precedence = ()  # No operator precedence needed for this structure

# The start rule for the parser
def p_program(p):
    '''program : include_statement function_definition'''
    print("Program parsed successfully.")

# Rule for include statements
def p_include_statement(p):
    '''include_statement : INCLUDE HEADER'''
    #print(f"Include statement detected: {p[2]}")

# Rule for function definition, including braces for the body
def p_function_definition(p):
    '''function_definition : KEYWORD IDENTIFIER LPAREN RPAREN PUNCTUATION statement_block'''
    print("Function definition detected.")

# Rule for a block of statements within curly braces
def p_statement_block(p):
    '''statement_block : PUNCTUATION statements PUNCTUATION'''
    pass

# Rule for multiple statements in function body
def p_statements(p):
    '''statements : statement statements
                  | statement'''
    pass

# Rule for individual statements
def p_statement(p):
    '''statement : statement_declare
                 | statement_assign
                 | statement_printf
                 | statement_return'''
    pass

# Rule for declaring variables
def p_statement_declare(p):
    '''statement_declare : KEYWORD IDENTIFIER PUNCTUATION'''
    var_type = p[1]
    var_name = p[2]
    if var_name in symbol_table:
        print(f"Semantic error: the variable '{var_name}' is already declared.")
    else:
        symbol_table[var_name] = var_type
        print(f"Declaration detected: {var_name} of the type {var_type}")

# Rule for assigning values to variables
def p_statement_assign(p):
    '''statement_assign : IDENTIFIER OPERATOR NUMBER PUNCTUATION'''
    var_name = p[1]
    if var_name not in symbol_table:
        print(f"Semantic error: the variable '{var_name}' has not been declared yet.")
    else:
        print(f"Valid assignment: {var_name} = {p[3]}")

# Rule for printf statements
def p_statement_printf(p):
    '''statement_printf : KEYWORD LPAREN STRING RPAREN PUNCTUATION'''
    print(f"Printf statement detected with message: {p[3]}")

# Rule for return statements
def p_statement_return(p):
    '''statement_return : KEYWORD NUMBER PUNCTUATION'''
    print(f"Return statement detected with value: {p[2]}")

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

# Build the parser
yacc.yacc()

# Test lexer and parser with the input
data = '''#include <stdio.h>
int main() {
    int a;
    a = 5;
    printf("Hola, mundo!\n");
    return 0;
}'''

# Tokenize and parse the input
lexer.input(data)
while True:
    token = lexer.token()
    if not token:
        break
    print(token)

# Parse
result = yacc.parse(data)
print(result)