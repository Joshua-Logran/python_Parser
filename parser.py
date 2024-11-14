import ply.lex as lex  # Import lexical analysis module from PLY
import ply.yacc as yacc  # Import syntax analysis module from PLY
import sys  # Import system-specific parameters and functions

flag_lexical_error = False  # Flag indicating if a lexical error has occurred
flag_sintax_error = False  # Flag indicating if a syntax error has occurred
flag_semantic_error = False  # Flag indicating if a semantic error has occurred

result = 0  # Variable to store parsing result
symbol_table = {}  # Dictionary to store variable names and types

# Token list for lexical analysis
tokens = (
    'PUNCTUATION', 'OPERATOR', 'LITERAL', 'KEYWORD', 'IDENTIFIER', 'NUMBER',
    'INCLUDE', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULUS', 'EXPONENT'
)

# C keywords, except 'main' so it can be treated as an identifier
keywords = {
    'int': 'KEYWORD',
    'return': 'KEYWORD',
    'char': 'KEYWORD',
    'float': 'KEYWORD',
    'double': 'KEYWORD',
    'void': 'KEYWORD',
}

# Regular expression for punctuation tokens
t_PUNCTUATION = r'[;{}()]'  # Matches punctuation symbols
t_OPERATOR = r'='  # Matches the assignment operator
t_INCLUDE = r'\#include\s+<\w+\.h>'  # Matches #include statements

# Operators for arithmetic expressions
t_PLUS = r'\+'  # Matches the addition operator
t_MINUS = r'-'  # Matches the subtraction operator
t_TIMES = r'\*'  # Matches the multiplication operator
t_DIVIDE = r'/'  # Matches the division operator
t_MODULUS = r'%'  # Matches the modulus operator
t_EXPONENT = r'\^'  # Matches the exponentiation operator

# Regular expression for string literals
def t_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''  # Matches double-quoted or single-quoted strings
    return t  # Return the token

# Regular expression for identifiers (variables or keywords)
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'  # Matches a variable or keyword name
    t.type = keywords.get(t.value, 'IDENTIFIER')  # Check if identifier is a keyword
    return t  # Return the token

# Regular expression for numbers
def t_NUMBER(t):
    r'\d+'  # Matches one or more digits
    t.value = int(t.value)  # Convert to integer
    return t  # Return the token

# Ignore spaces and tabs
t_ignore = ' \t'  # Specifies that spaces and tabs should be ignored

# Rule to handle newlines
def t_newline(t):
    r'\n+'  # Matches one or more newline characters
    t.lexer.lineno += len(t.value)  # Increments line number by the number of newlines

# Rule to handle lexical errors
def t_error(t):
    print(f"Illegal character '{t.value[0]}' on line {t.lineno}")  # Print error message for illegal character
    t.lexer.skip(1)  # Skip the illegal character
    global flag_lexical_error  # Access global lexical error flag
    flag_lexical_error = True  # Set the lexical error flag to True

# Build the lexer
lexer = lex.lex()  # Initialize the lexer

# Grammar rule for the main program structure
def p_program(p):
    '''program : INCLUDE function'''  # A program consists of an include statement and a function

# Grammar rule for function definition
def p_function(p):
    '''function : KEYWORD IDENTIFIER PUNCTUATION PUNCTUATION block'''  # A function has a keyword, identifier, and block

# Grammar rule for a code block
def p_block(p):
    '''block : PUNCTUATION declarations statements return_statement PUNCTUATION'''  # A block includes declarations, statements, and return

# Grammar rule for declarations
def p_declarations(p):
    '''declarations : declaration PUNCTUATION
                    | declarations declaration PUNCTUATION'''  # Declarations are recursive

# Grammar rule for a single declaration
def p_declaration(p):
    '''declaration : KEYWORD IDENTIFIER'''  # A declaration consists of a type keyword and identifier
    var_type = p[1]  # Store the type of the variable
    var_name = p[2]  # Store the name of the variable
    if var_name in symbol_table:  # Check if the variable is already declared
        print(f"Semantic error: the variable '{var_name}' is already declared.")  # Print semantic error message
        global flag_semantic_error  # Access the global semantic error flag
        flag_semantic_error = True  # Set the semantic error flag to True
    else:
        symbol_table[var_name] = var_type  # Add variable to symbol table with its type

# Grammar rule for statements
def p_statements(p):
    '''statements : statement PUNCTUATION
                  | statements statement PUNCTUATION'''  # Statements are recursive

# Grammar rules for arithmetic operations
def p_operation(p):
    '''operation : NUMBER PLUS NUMBER
                 | NUMBER MINUS NUMBER
                 | NUMBER TIMES NUMBER
                 | NUMBER DIVIDE NUMBER
                 | NUMBER MODULUS NUMBER
                 | NUMBER EXPONENT NUMBER'''  # Matches basic arithmetic operations
    p[1] = int(p[1])  # Convert first operand to integer
    p[3] = int(p[3])  # Convert second operand to integer
    if p[2] == '+':  # If operator is +
        p[0] = p[1] + p[3]  # Perform addition
    elif p[2] == '-':  # If operator is -
        p[0] = p[1] - p[3]  # Perform subtraction
    elif p[2] == '*':  # If operator is *
        p[0] = p[1] * p[3]  # Perform multiplication
    elif p[2] == '/':  # If operator is /
        p[0] = p[1] / p[3]  # Perform division
    elif p[2] == '%':  # If operator is %
        p[0] = p[1] % p[3]  # Perform modulus
    elif p[2] == '^':  # If operator is ^
        p[0] = p[1] ** p[3]  # Perform exponentiation

# Grammar rule for a statement
def p_statement(p):
    '''statement : assignment_statement
                 | IDENTIFIER PUNCTUATION LITERAL PUNCTUATION
                 | assignment_operation'''  # Statements can be assignments or operations

# Grammar rule for assignment statements
def p_assignment_statement(p):
    ''' assignment_statement : IDENTIFIER OPERATOR NUMBER 
                             | IDENTIFIER OPERATOR LITERAL'''  # Matches assignments
    var_name = p[1]  # Get the variable name
    global flag_semantic_error  # Access global semantic error flag
    if var_name not in symbol_table:  # Check if the variable is declared
        print(f"Semantic error: the variable '{var_name}' has not been declared yet.")  # Print error if undeclared
        flag_semantic_error = True  # Set the semantic error flag
    else:
        var_type = str(symbol_table[var_name])  # Get type of the variable
        expr_type = type(p[3]).__name__  # Type of expression being assigned
        if var_type != expr_type:  # Check for type mismatch
            print(f"Semantic error: can't assign a value of type '{expr_type}' to the variable '{var_name}' of type '{var_type}'.")  # Print error message
            flag_semantic_error = True  # Set the semantic error flag

# Grammar rule for operations within assignments
def p_assignment_operation(p):
    '''assignment_operation : IDENTIFIER OPERATOR operation'''  # Matches assignments with operations
    var_name = p[1]  # Get the variable name
    global flag_semantic_error  # Access global semantic error flag
    if var_name not in symbol_table:  # Check if variable is declared
        print(f"Semantic error: the variable '{var_name}' has not been declared yet.")  # Print undeclared variable error
        flag_semantic_error = True  # Set the semantic error flag
    else:
        var_type = str(symbol_table[var_name])  # Get the type of the variable
        expr_type = type(p[3]).__name__  # Type of the operation result
        if var_type != expr_type:  # Check for type mismatch
            print(f"Semantic error: can't assign a value of type '{expr_type}' to the variable '{var_name}' of type '{var_type}'.")  # Print error message
            flag_semantic_error = True  # Set the semantic error flag

# Grammar rule for return statements
def p_return_statement(p):
    '''return_statement : KEYWORD NUMBER PUNCTUATION'''  # Matches return statements

# Rule to handle syntax errors
def p_error(p):
    global flag_sintax_error, flag_semantic_error  # Access the global syntax error flag
    flag_sintax_error = True  # Set the syntax error flag
    flag_semantic_error = True  # Set the semantic error flag

    if p:  # If the error is in a specific token
        print(f"Syntax error in '{p.value}'")  # Print the error message
    else:  # If the error is at the end of the input
        print("Syntax error at the end of the file")  # Print end of file error

# Build the parser
parser = yacc.yacc(debug=True, write_tables=True)  # Initialize the parser

# Main function to process a file
def main():
    if len(sys.argv) != 2:  # Check if the filename argument is provided
        print(f"Usage: {sys.argv[0]} <file.c>")  # Print usage instructions
        sys.exit(1)  # Exit if filename is missing
    
    filename = sys.argv[1]  # Get the filename from arguments
    try:
        with open(filename, "r") as file:  # Open the file for reading
            code_lines = file.readlines()  # Read all lines from the file
    except IOError as e:  # Handle file reading error
        print(f"Error reading file {filename}: {e}")  # Print the error message
        sys.exit(1)  # Exit on file read error
    
    code = ''.join(code_lines)  # Join all lines into a single string
    lexer.input(code)  # Pass the code as a single string to the lexer
    while True:
        tok = lexer.token()  # Generate tokens
        if not tok:  # Stop if no tokens are left
            break
    
    if flag_lexical_error:  # Check if lexical errors were found
        print("Lexing error")  # Print lexical error message
    else:
        print("Syntactic analysis result:")  # Begin syntactic analysis output
        parser.parse(code)  # Run the parser
        if flag_sintax_error and flag_semantic_error:  # Check for syntax and semantic errors
            print("Parsing error")  # Print parsing error message
            print("SDT error")  # Print SDT error message
        elif not flag_sintax_error and flag_semantic_error:  # If only semantic errors occurred
            print("Parsing success")  # Print parsing success message
            print("SDT error")  # Print SDT error message
        else:
            print("Parsing success")  # Print full parsing success message
            print("SDT Verified")  # Print SDT verified message

# Program entry point
if __name__ == "__main__":
    main()  # Call the main function