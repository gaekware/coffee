import sys

# Definições de classes de caracteres para simplificar a tabela de transição
def get_char_class(char):
    if char.isalpha() or char == '_': return 'letra'
    if char.isdigit(): return 'digito'
    if char == '.': return 'ponto'
    if char == '"': return 'aspas'
    if char in ' \t\r\n': return 'espaco'
    return char # Retorna o próprio caractere para operadores e delimitadores

# Tabela de transições do AFD (baseada no diagrama Mermaid)
# Formato: dfa_table[estado_atual][classe_do_char] = proximo_estado
DFA_TABLE = {
    'S0': {'letra': 'S1_ID', 'digito': 'S2_NUM', '>': 'S4_GT', '<': 'S5_LT', '=': 'S6_EQ', '!': 'S7_NE', 'aspas': 'S8_STR', '(': 'S9_LPAREN', ')': 'S10_RPAREN', ',': 'S11_COMMA', '#': 'S12_COMMENT'},
    'S1_ID': {'letra': 'S1_ID', 'digito': 'S1_ID'},
    'S2_NUM': {'digito': 'S2_NUM', 'ponto': 'S3_FLOAT'},
    'S3_FLOAT': {'digito': 'S3_FLOAT_NUM'},
    'S3_FLOAT_NUM': {'digito': 'S3_FLOAT_NUM'},
    'S4_GT': {'=': 'S4_GE'},
    'S5_LT': {'=': 'S5_LE'},
    'S6_EQ': {'=': 'S6_EQEQ'},
    'S7_NE': {'=': 'S7_NE_EQ'},
    'S8_STR': {'aspas': 'S8_END_STR'}, # Transição para qualquer outro char é implícita
    'S12_COMMENT': {}, # Transição para qualquer char exceto \n é implícita
}

# Mapeia estados de aceitação para tipos de token
ACCEPTING_STATES = {
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
}

KEYWORDS = {'load', 'filter', 'select', 'display', 'where'}

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.col = 1

    def next_token(self):
        while self.position < len(self.source):
            char = self.source[self.position]

            if get_char_class(char) == 'espaco':
                if char == '\n':
                    self.line += 1
                    self.col = 1
                else:
                    self.col += 1
                self.position += 1
                continue

            current_state = 'S0'
            lexeme = ""
            last_accepted_state = None
            last_accepted_position = self.position

            temp_pos = self.position
            while temp_pos < len(self.source):
                char_to_process = self.source[temp_pos]
                char_class = get_char_class(char_to_process)
                
                # Tratamento especial para strings e comentários
                if current_state == 'S8_STR' and char_class != 'aspas':
                    next_state = 'S8_STR'
                elif current_state == 'S12_COMMENT' and char_to_process != '\n':
                    next_state = 'S12_COMMENT'
                else:
                    next_state = DFA_TABLE.get(current_state, {}).get(char_class)

                if next_state is None:
                    break # Fim do token (nenhuma transição)
                
                current_state = next_state
                temp_pos += 1
                
                if current_state in ACCEPTING_STATES:
                    last_accepted_state = current_state
                    last_accepted_position = temp_pos
            
            if last_accepted_state is None:
                # Se nenhum estado de aceitação foi alcançado, é um erro
                raise ValueError(f"Erro Léxico: Token inválido '{self.source[self.position]}' na linha {self.line}, coluna {self.col}")

            lexeme = self.source[self.position:last_accepted_position]
            token_type = ACCEPTING_STATES[last_accepted_state]

            # Atualiza a posição e coluna
            self.col += len(lexeme)
            self.position = last_accepted_position

            # Descarta comentários
            if last_accepted_state == 'S12_COMMENT':
                continue
            
            # Verifica se um IDENTIFIER é uma KEYWORD
            if token_type == 'IDENTIFIER' and lexeme in KEYWORDS:
                token_type = 'KEYWORD'
            
            return (lexeme, token_type)

        return None # Fim do arquivo

# Bloco de execução principal
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
        
    lexer = Lexer(code)
    print(f"Analisando o arquivo: {file_path}\n")
    print(f"| {'Token'.ljust(20)} | {'Tipo'.ljust(15)} |")
    print(f"+{'-'*22}+{'-'*17}+")
    
    try:
        while (token := lexer.next_token()):
            print(f"| {token[0].ljust(20)} | {token[1].ljust(15)} |")
    except ValueError as e:
        print(e)