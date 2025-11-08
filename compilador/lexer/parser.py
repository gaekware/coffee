import sys

def get_char_class(char):
    if char.isalpha() or char == '_': return 'letra'
    if char.isdigit(): return 'digito'
    if char == '.': return 'ponto'
    if char == '"': return 'aspas'
    if char in ' \t\r': return 'espaco'
    if char == '\n': return 'novalinha'
    if char in '()#': return char
    if char in '><=!': return char
    return 'outro'

DFA_TRANSITIONS = {
    'S0': {
        'letra': 'S1_ID', 'digito': 'S2_NUM', '>': 'S4_GT', '<': 'S5_LT',
        '=': 'S6_EQ', '!': 'S7_NE', '"': 'S8_STR', '(': 'S9_LPAREN',
        ')': 'S10_RPAREN', ',': 'S11_COMMA', '#': 'S12_COMMENT',
        'espaco': 'S13_SPACE', 'novalinha': 'S14_NEWLINE'
    },
    'S1_ID': {'letra': 'S1_ID', 'digito': 'S1_ID', '_': 'S1_ID'},
    'S2_NUM': {'digito': 'S2_NUM', 'ponto': 'S3_FLOAT'},
    'S3_FLOAT': {'digito': 'S3_FLOAT_NUM'},
    'S3_FLOAT_NUM': {'digito': 'S3_FLOAT_NUM'},
    'S4_GT': {'=': 'S4_GE'},
    'S5_LT': {'=': 'S5_LE'},
    'S6_EQ': {'=': 'S6_EQEQ'},
    'S7_NE': {'=': 'S7_NE_EQ'},
    'S8_STR': {'"': 'S8_END_STR', 'outro': 'S8_STR', 'letra': 'S8_STR', 'digito': 'S8_STR', 'espaco': 'S8_STR', 'ponto': 'S8_STR', 'novalinha': 'S8_STR', '(': 'S8_STR', ')': 'S8_STR', ',': 'S8_STR', '#': 'S8_STR', '>': 'S8_STR', '<': 'S8_STR', '=': 'S8_STR', '!': 'S8_STR'},
    'S12_COMMENT': {'letra': 'S12_COMMENT', 'digito': 'S12_COMMENT', 'outro': 'S12_COMMENT', 'espaco': 'S12_COMMENT', 'ponto': 'S12_COMMENT', '"': 'S12_COMMENT', '(': 'S12_COMMENT', ')': 'S12_COMMENT', ',': 'S12_COMMENT', '>': 'S12_COMMENT', '<': 'S12_COMMENT', '=': 'S12_COMMENT', '!': 'S12_COMMENT'},
    'S13_SPACE': {'espaco': 'S13_SPACE'},
}


DFA_ACCEPTING_STATES = {
    'S1_ID': 'IDENTIFIER',
    'S2_NUM': 'NUMBER',
    'S3_FLOAT_NUM': 'NUMBER',
    'S4_GT': 'GT',
    'S4_GE': 'GE',
    'S5_LT': 'LT',
    'S5_LE': 'LE',
    'S6_EQ': 'ASSIGN',
    'S6_EQEQ': 'EQEQ',
    'S7_NE_EQ': 'NE',
    'S8_END_STR': 'STRING',
    'S9_LPAREN': 'LPAREN',
    'S10_RPAREN': 'RPAREN',
    'S11_COMMA': 'COMMA',
    'S12_COMMENT': 'COMMENT',
    'S13_SPACE': 'WHITESPACE',
    'S14_NEWLINE': 'NEWLINE',
}

KEYWORDS = {'load', 'filter', 'select', 'display', 'where'}

class Token:
    def __init__(self, type, value, line, col):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, L{self.line}:C{self.col})"

class DFA:
    def __init__(self, transitions, accepting_states):
        self.transitions = transitions
        self.accepting_states = accepting_states

    def run(self, input_string):
        """
        Executa o AFD na string de entrada e retorna o lexema mais longo
        e seu tipo de token correspondente.
        """
        current_state = 'S0'
        last_accepted_info = None

        for i, char in enumerate(input_string):
            char_class = get_char_class(char)
            
            if char in self.transitions.get(current_state, {}):
                current_state = self.transitions[current_state][char]
            elif char_class in self.transitions.get(current_state, {}):
                current_state = self.transitions[current_state][char_class]
            else:
                break

            if current_state in self.accepting_states:
                last_accepted_info = {
                    "state": current_state,
                    "position": i + 1
                }

        if last_accepted_info is None:
            if current_state == 'S8_STR':
                raise ValueError("String não fechada")
            raise ValueError(f"Token inválido começando com '{input_string[0]}'")

        lexeme = input_string[:last_accepted_info["position"]]
        token_type = self.accepting_states[last_accepted_info["state"]]
        return lexeme, token_type

class Lexer:
    def __init__(self, source_code, dfa):
        self.source = source_code
        self.dfa = dfa
        self.position = 0
        self.line = 1
        self.col = 1

    def next_token(self):
        while self.position < len(self.source):
            remaining_code = self.source[self.position:]
            
            start_line = self.line
            start_col = self.col

            try:
                lexeme, token_type = self.dfa.run(remaining_code)
            except ValueError as e:
                raise ValueError(f"{e} na linha {start_line}, coluna {start_col}")

            self.position += len(lexeme)
            lines_in_lexeme = lexeme.count('\n')
            if lines_in_lexeme > 0:
                self.line += lines_in_lexeme
                self.col = len(lexeme) - lexeme.rfind('\n')
            else:
                self.col += len(lexeme)

            if token_type in ['WHITESPACE', 'COMMENT', 'NEWLINE']:
                continue

            if token_type == 'IDENTIFIER' and lexeme in KEYWORDS:
                token_type = lexeme.upper()
           
            return Token(token_type, lexeme, start_line, start_col)

        return Token('EOF', None, self.line, self.col)


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()

    def error(self, expected_type):
        tok = self.current_token
        raise SyntaxError(
            f"Erro de Sintaxe: Esperava '{expected_type}', mas encontrou '{tok.value}' ({tok.type}) "
            f"na linha {tok.line}, coluna {tok.col}"
        )

    def eat(self, expected_type):
        """
        Consome o token atual se ele for do tipo esperado.
        Se for, avança para o próximo token.
        Se não for, lança um erro.
        """
        if self.current_token.type == expected_type:
            self.current_token = self.lexer.next_token()
        else:
            self.error(expected_type)

    def parse(self):
        """Ponto de entrada principal do parser."""
        self.program()
        if self.current_token.type != 'EOF':
            tok = self.current_token
            raise SyntaxError(
                f"Erro de Sintaxe: Código inesperado no final do programa. "
                f"Token '{tok.value}' ({tok.type}) na linha {tok.line}, coluna {tok.col}"
            )
        return True

    def program(self):
        """<Program> ::= <StatementList>"""
        self.statement_list()

    def statement_list(self):
        """<StatementList> ::= { <Statement> }"""
        while self.current_token.type != 'EOF':
            self.statement()

    def statement(self):
        """<Statement> ::= <DisplayStatement> | <AssignmentStatement>"""
        if self.current_token.type == 'DISPLAY':
            self.display_statement()
        elif self.current_token.type == 'IDENTIFIER':
            self.assignment_statement()
        else:
            tok = self.current_token
            raise SyntaxError(
                f"Erro de Sintaxe: Comando inválido. Esperava 'display' ou um nome de variável, "
                f"mas encontrou '{tok.value}' ({tok.type}) na linha {tok.line}, coluna {tok.col}"
            )

    def display_statement(self):
        """<DisplayStatement> ::= "display" identifier"""
        self.eat('DISPLAY')
        self.eat('IDENTIFIER')

    def assignment_statement(self):
        """<AssignmentStatement> ::= identifier "=" <AssignmentRHS>"""
        self.eat('IDENTIFIER')
        self.eat('ASSIGN')
        self.assignment_rhs()

    def assignment_rhs(self):
        """
        <AssignmentRHS> ::= <LoadInvocation> 
                          | <FilterRHS> 
                          | <SelectRHS>
        """
        if self.current_token.type == 'LOAD':
            self.load_invocation()
        elif self.current_token.type == 'FILTER':
            self.filter_rhs()
        elif self.current_token.type == 'SELECT':
            self.select_rhs()
        else:
            self.error("'load', 'filter' ou 'select' após o '='")

    def load_invocation(self):
        """<LoadInvocation> ::= "load" string_literal"""
        self.eat('LOAD')
        self.eat('STRING')

    def filter_rhs(self):
        """<FilterRHS> ::= "filter" identifier "where" <LogicalExpression>"""
        self.eat('FILTER')
        self.eat('IDENTIFIER')
        self.eat('WHERE')
        self.logical_expression()

    def select_rhs(self):
        """<SelectRHS> ::= "select" identifier "(" <ColumnList> ")" """
        self.eat('SELECT')
        self.eat('IDENTIFIER')
        self.eat('LPAREN')
        self.column_list()
        self.eat('RPAREN')

    def column_list(self):
        """<ColumnList> ::= identifier { "," identifier }"""
        self.eat('IDENTIFIER')
        while self.current_token.type == 'COMMA':
            self.eat('COMMA')
            self.eat('IDENTIFIER')

    def logical_expression(self):
        """<LogicalExpression> ::= <RelationalExpression>"""
        self.relational_expression()

    def relational_expression(self):
        """<RelationalExpression> ::= <Term> <RelationalOp> <Term>"""
        self.term()
        self.relational_op()
        self.term()

    def relational_op(self):
        """<RelationalOp> ::= ">" | "<" | "==" | "!=" | ">=" | "<=" """
        if self.current_token.type in ('GT', 'GE', 'LT', 'LE', 'EQEQ', 'NE'):
            self.eat(self.current_token.type)
        else:
            self.error("Operador Relacional (como '>', '==', etc.)")

    def term(self):
        """<Term> ::= identifier | number_literal | string_literal"""
        if self.current_token.type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
        elif self.current_token.type == 'NUMBER':
            self.eat('NUMBER')
        elif self.current_token.type == 'STRING':
            self.eat('STRING')
        else:
            self.error("identificador, número ou string")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python parser.py <caminho_para_o_arquivo.coffee>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        with open(file_path, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        sys.exit(1)

    print(f"Analisando o arquivo: {file_path}\n")

    try:
        coffee_dfa = DFA(DFA_TRANSITIONS, DFA_ACCEPTING_STATES)
        lexer = Lexer(code, coffee_dfa)
        parser = Parser(lexer)
        parser.parse()
        
        print("="*30)
        print("SUCESSO: A sintaxe do programa está correta!")
        print("="*30)

    except (ValueError, SyntaxError) as e:
        print("="*30)
        print(f"FALHA NA COMPILAÇÃO:\n{e}")
        print("="*30)
        sys.exit(1)