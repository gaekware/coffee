import sys

# Definições de classes de caracteres para simplificar a tabela de transição
def get_char_class(char):
    if char.isalpha() or char == '_': return 'letra'
    if char.isdigit(): return 'digito'
    if char == '.': return 'ponto'
    if char == '"': return 'aspas'
    if char in ' \t\r': return 'espaco' 
    if char == '\n': return 'novalinha'
    return 'outro'

# Tabela de transições do AFD (baseada no diagrama Mermaid)
# Formato: dfa_table[estado_atual][classe_do_char] = proximo_estado
DFA_TRANSITIONS = {
    'S0': {'letra': 'S1_ID', 'digito': 'S2_NUM', '>': 'S4_GT', '<': 'S5_LT', '=': 'S6_EQ', '!': 'S7_NE', 'aspas': 'S8_STR', '(': 'S9_LPAREN', ')': 'S10_RPAREN', ',': 'S11_COMMA', '#': 'S12_COMMENT', 'espaco': 'S13_SPACE', 'novalinha': 'S14_NEWLINE'},
    'S1_ID': {'letra': 'S1_ID', 'digito': 'S1_ID'},
    'S2_NUM': {'digito': 'S2_NUM', 'ponto': 'S3_FLOAT'},
    'S3_FLOAT': {'digito': 'S3_FLOAT_NUM'},
    'S3_FLOAT_NUM': {'digito': 'S3_FLOAT_NUM'},
    'S4_GT': {'=': 'S4_GE'},
    'S5_LT': {'=': 'S5_LE'},
    'S6_EQ': {'=': 'S6_EQEQ'},
    'S7_NE': {'=': 'S7_NE_EQ'},
    'S8_STR': {'aspas': 'S8_END_STR', 'letra': 'S8_STR', 'digito': 'S8_STR', 'outro': 'S8_STR', 'espaco': 'S8_STR'},
    'S12_COMMENT': {'letra': 'S12_COMMENT', 'digito': 'S12_COMMENT', 'outro': 'S12_COMMENT', 'espaco': 'S12_COMMENT'},
    'S13_SPACE': {'espaco': 'S13_SPACE'},
}

# Mapeia estados de aceitação para tipos de token
DFA_ACCEPTING_STATES = {
    'S1_ID': 'IDENTIFIER',
    'S2_NUM': 'NUMBER',
    'S3_FLOAT_NUM': 'NUMBER',
    'S4_GT': 'OP_REL',
    'S4_GE': 'OP_REL',
    'S5_LT': 'OP_REL',
    'S5_LE': 'OP_REL',
    'S6_EQ': 'OP_ASSIGN',
    'S6_EQEQ': 'OP_REL',
    'S7_NE_EQ': 'OP_REL',
    'S8_END_STR': 'STRING',
    'S9_LPAREN': 'LPAREN',
    'S10_RPAREN': 'RPAREN',
    'S11_COMMA': 'COMMA',
    'S12_COMMENT': 'COMMENT',
    'S13_SPACE': 'WHITESPACE',
    'S14_NEWLINE': 'NEWLINE',
}

KEYWORDS = {'load', 'filter', 'select', 'display', 'where'}

class DFA:
    """Encapsula a lógica para executar um Autômato Finito Determinístico."""
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
        
        # Percorre a string para encontrar o "match" mais longo
        for i, char in enumerate(input_string):
            char_class = get_char_class(char)
            
            # Casos especiais que não estão na tabela principal para simplificar
            if char in self.transitions.get(current_state, {}):
                current_state = self.transitions[current_state][char]
            elif char_class in self.transitions.get(current_state, {}):
                current_state = self.transitions[current_state][char_class]
            else:
                break # Nenhuma transição, fim do token
            
            # Se o estado atual for de aceitação, salve-o
            if current_state in self.accepting_states:
                last_accepted_info = {
                    "state": current_state,
                    "position": i + 1
                }
        
        if last_accepted_info is None:
            # Não foi possível reconhecer nenhum token
            raise ValueError(f"Token inválido começando com '{input_string[0]}'")

        # Retorna o lexema e o tipo do último estado de aceitação válido
        lexeme = input_string[:last_accepted_info["position"]]
        token_type = self.accepting_states[last_accepted_info["state"]]
        return lexeme, token_type

class Lexer:
    """Gerencia o processo de tokenização do código-fonte."""
    def __init__(self, source_code, dfa):
        self.source = source_code
        self.dfa = dfa
        self.position = 0
        self.line = 1
        self.col = 1

    def next_token(self):
        """Retorna o próximo token válido do código-fonte."""
        while self.position < len(self.source):
            remaining_code = self.source[self.position:]
            
            try:
                lexeme, token_type = self.dfa.run(remaining_code)
            except ValueError as e:
                # Adiciona contexto de linha/coluna ao erro do DFA
                raise ValueError(f"{e} na linha {self.line}, coluna {self.col}")

            # Atualiza posição, linha e coluna
            self.position += len(lexeme)
            lines_in_lexeme = lexeme.count('\n')
            if lines_in_lexeme > 0:
                self.line += lines_in_lexeme
                # Encontra a posição da última nova linha para resetar a coluna
                self.col = len(lexeme) - lexeme.rfind('\n')
            else:
                self.col += len(lexeme)

            # Ignora tokens que não são relevantes para o parser
            if token_type in ['WHITESPACE', 'COMMENT', 'NEWLINE']:
                continue
            
            # Converte IDENTIFIER para KEYWORD, se aplicável
            if token_type == 'IDENTIFIER' and lexeme in KEYWORDS:
                token_type = 'KEYWORD'

            return (lexeme, token_type)

        return None # Fim do arquivo (End of File)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python lexer.py <caminho_para_o_arquivo.coffee>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        with open(file_path, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        sys.exit(1)
        
    # 1. Cria a instância do DFA
    coffee_dfa = DFA(DFA_TRANSITIONS, DFA_ACCEPTING_STATES)
    
    # 2. Cria a instância do Lexer, injetando o DFA
    lexer = Lexer(code, coffee_dfa)
    
    # 3. Processa e imprime os tokens
    print(f"Analisando o arquivo: {file_path}\n")
    print(f"| {'Token'.ljust(20)} | {'Tipo'.ljust(15)} |")
    print(f"+{'-'*22}+{'-'*17}+")
    
    try:
        while (token := lexer.next_token()):
            print(f"| {token[0].ljust(20)} | {token[1].ljust(15)} |")
    except ValueError as e:
        print(e)