import sys
from abc import ABC, abstractmethod

"""
PARSER COM CONSTRUÇÃO DE AST PARA LINGUAGEM COFFEE
=================================================

Este parser implementa análise sintática descendente recursiva (LL(1))
e constrói uma Árvore Sintática Abstrata (AST) para ser consumida 
pela fase de análise semântica.

Estrutura da AST:
- ProgramNode: nó raiz contendo lista de statements
- StatementNode: classe base para comandos (display, assignment)
- ExpressionNode: classe base para expressões (load, filter, select)
- TermNode: nós folha (identificadores, números, strings)
- RelationalExpressionNode: nós para comparações

A AST construída preserva a estrutura hierárquica do programa
e facilita a análise semântica posterior.
"""

# ===== AST NODE CLASSES =====

class ASTNode(ABC):
    """Classe base abstrata para todos os nós da AST"""
    pass

class ProgramNode(ASTNode):
    """Nó raiz do programa - contém lista de statements"""
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"Program({self.statements})"

class StatementNode(ASTNode):
    """Classe base para todos os statements"""
    pass

class DisplayStatementNode(StatementNode):
    """Nó para comando display"""
    def __init__(self, identifier):
        self.identifier = identifier
    
    def __repr__(self):
        return f"Display({self.identifier})"

class AssignmentStatementNode(StatementNode):
    """Nó para comando de atribuição"""
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
    
    def __repr__(self):
        return f"Assignment({self.identifier} = {self.expression})"

class ExpressionNode(ASTNode):
    """Classe base para expressões"""
    pass

class LoadExpressionNode(ExpressionNode):
    """Nó para expressão load"""
    def __init__(self, file_path):
        self.file_path = file_path
    
    def __repr__(self):
        return f"Load({self.file_path})"

class FilterExpressionNode(ExpressionNode):
    """Nó para expressão filter"""
    def __init__(self, dataset, condition):
        self.dataset = dataset
        self.condition = condition
    
    def __repr__(self):
        return f"Filter({self.dataset}, {self.condition})"

class SelectExpressionNode(ExpressionNode):
    """Nó para expressão select"""
    def __init__(self, dataset, columns):
        self.dataset = dataset
        self.columns = columns
    
    def __repr__(self):
        return f"Select({self.dataset}, {self.columns})"

class RelationalExpressionNode(ExpressionNode):
    """Nó para expressão relacional (comparação)"""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"

class TermNode(ASTNode):
    """Nó para termos (identificadores, números, strings)"""
    def __init__(self, value, term_type):
        self.value = value
        self.type = term_type  # 'IDENTIFIER', 'NUMBER', 'STRING'
    
    def __repr__(self):
        return f"{self.type}({self.value})"

# ===== LEXER CLASSES =====

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
        Se for, avança para o próximo token e retorna o token consumido.
        Se não for, lança um erro.
        """
        if self.current_token.type == expected_type:
            token = self.current_token
            self.current_token = self.lexer.next_token()
            return token
        else:
            self.error(expected_type)

    def parse(self):
        """Ponto de entrada principal do parser. Retorna a AST."""
        ast = self.program()
        if self.current_token.type != 'EOF':
            tok = self.current_token
            raise SyntaxError(
                f"Erro de Sintaxe: Código inesperado no final do programa. "
                f"Token '{tok.value}' ({tok.type}) na linha {tok.line}, coluna {tok.col}"
            )
        return ast

    def program(self):
        """<Program> ::= <StatementList>"""
        statements = self.statement_list()
        return ProgramNode(statements)

    def statement_list(self):
        """<StatementList> ::= { <Statement> }"""
        statements = []
        while self.current_token.type != 'EOF':
            stmt = self.statement()
            statements.append(stmt)
        return statements

    def statement(self):
        """<Statement> ::= <DisplayStatement> | <AssignmentStatement>"""
        if self.current_token.type == 'DISPLAY':
            return self.display_statement()
        elif self.current_token.type == 'IDENTIFIER':
            return self.assignment_statement()
        else:
            tok = self.current_token
            raise SyntaxError(
                f"Erro de Sintaxe: Comando inválido. Esperava 'display' ou um nome de variável, "
                f"mas encontrou '{tok.value}' ({tok.type}) na linha {tok.line}, coluna {tok.col}"
            )

    def display_statement(self):
        """<DisplayStatement> ::= "display" identifier"""
        self.eat('DISPLAY')
        identifier_token = self.eat('IDENTIFIER')
        return DisplayStatementNode(identifier_token.value)

    def assignment_statement(self):
        """<AssignmentStatement> ::= identifier "=" <AssignmentRHS>"""
        identifier_token = self.eat('IDENTIFIER')
        self.eat('ASSIGN')
        expression = self.assignment_rhs()
        return AssignmentStatementNode(identifier_token.value, expression)

    def assignment_rhs(self):
        """
        <AssignmentRHS> ::= <LoadInvocation> 
                          | <FilterRHS> 
                          | <SelectRHS>
        """
        if self.current_token.type == 'LOAD':
            return self.load_invocation()
        elif self.current_token.type == 'FILTER':
            return self.filter_rhs()
        elif self.current_token.type == 'SELECT':
            return self.select_rhs()
        else:
            self.error("'load', 'filter' ou 'select' após o '='")

    def load_invocation(self):
        """<LoadInvocation> ::= "load" string_literal"""
        self.eat('LOAD')
        string_token = self.eat('STRING')
        return LoadExpressionNode(string_token.value)

    def filter_rhs(self):
        """<FilterRHS> ::= "filter" identifier "where" <LogicalExpression>"""
        self.eat('FILTER')
        dataset_token = self.eat('IDENTIFIER')
        self.eat('WHERE')
        condition = self.logical_expression()
        return FilterExpressionNode(dataset_token.value, condition)

    def select_rhs(self):
        """<SelectRHS> ::= "select" identifier "(" <ColumnList> ")" """
        self.eat('SELECT')
        dataset_token = self.eat('IDENTIFIER')
        self.eat('LPAREN')
        columns = self.column_list()
        self.eat('RPAREN')
        return SelectExpressionNode(dataset_token.value, columns)

    def column_list(self):
        """<ColumnList> ::= identifier { "," identifier }"""
        columns = []
        first_column = self.eat('IDENTIFIER')
        columns.append(first_column.value)
        
        while self.current_token.type == 'COMMA':
            self.eat('COMMA')
            column_token = self.eat('IDENTIFIER')
            columns.append(column_token.value)
        
        return columns

    def logical_expression(self):
        """<LogicalExpression> ::= <RelationalExpression>"""
        return self.relational_expression()

    def relational_expression(self):
        """<RelationalExpression> ::= <Term> <RelationalOp> <Term>"""
        left = self.term()
        operator = self.relational_op()
        right = self.term()
        return RelationalExpressionNode(left, operator, right)

    def relational_op(self):
        """<RelationalOp> ::= ">" | "<" | "==" | "!=" | ">=" | "<=" """
        if self.current_token.type in ('GT', 'GE', 'LT', 'LE', 'EQEQ', 'NE'):
            op_token = self.eat(self.current_token.type)
            # Mapeia os tipos de token para símbolos legíveis
            op_map = {
                'GT': '>', 'GE': '>=', 'LT': '<', 
                'LE': '<=', 'EQEQ': '==', 'NE': '!='
            }
            return op_map[op_token.type]
        else:
            self.error("Operador Relacional (como '>', '==', etc.)")

    def term(self):
        """<Term> ::= identifier | number_literal | string_literal"""
        if self.current_token.type == 'IDENTIFIER':
            token = self.eat('IDENTIFIER')
            return TermNode(token.value, 'IDENTIFIER')
        elif self.current_token.type == 'NUMBER':
            token = self.eat('NUMBER')
            return TermNode(token.value, 'NUMBER')
        elif self.current_token.type == 'STRING':
            token = self.eat('STRING')
            return TermNode(token.value, 'STRING')
        else:
            self.error("identificador, número ou string")


def print_ast(node, indent=0):
    """Função auxiliar para imprimir a AST de forma hierárquica e legível"""
    spaces = "  " * indent
    
    if isinstance(node, ProgramNode):
        print(f"{spaces}Program:")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)
    
    elif isinstance(node, DisplayStatementNode):
        print(f"{spaces}Display: {node.identifier}")
    
    elif isinstance(node, AssignmentStatementNode):
        print(f"{spaces}Assignment:")
        print(f"{spaces}  Variable: {node.identifier}")
        print(f"{spaces}  Expression:")
        print_ast(node.expression, indent + 2)
    
    elif isinstance(node, LoadExpressionNode):
        print(f"{spaces}Load: {node.file_path}")
    
    elif isinstance(node, FilterExpressionNode):
        print(f"{spaces}Filter:")
        print(f"{spaces}  Dataset: {node.dataset}")
        print(f"{spaces}  Condition:")
        print_ast(node.condition, indent + 2)
    
    elif isinstance(node, SelectExpressionNode):
        print(f"{spaces}Select:")
        print(f"{spaces}  Dataset: {node.dataset}")
        print(f"{spaces}  Columns: {', '.join(node.columns)}")
    
    elif isinstance(node, RelationalExpressionNode):
        print(f"{spaces}Comparison ({node.operator}):")
        print(f"{spaces}  Left:")
        print_ast(node.left, indent + 2)
        print(f"{spaces}  Right:")
        print_ast(node.right, indent + 2)
    
    elif isinstance(node, TermNode):
        print(f"{spaces}{node.type}: {node.value}")
    
    else:
        print(f"{spaces}Unknown node: {node}")


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
        ast = parser.parse()
        
        print("="*50)
        print("SUCESSO: Análise sintática concluída!")
        print("="*50)
        print("\nÁrvore Sintática Abstrata (AST):")
        print("-" * 40)
        print_ast(ast)
        print("\nAST construída com sucesso! Pronta para análise semântica.")
        print("="*50)

    except (ValueError, SyntaxError) as e:
        print("="*30)
        print(f"FALHA NA COMPILAÇÃO:\n{e}")
        print("="*30)
        sys.exit(1)