import re
import sys

# Especificação dos tokens usando Expressões Regulares, conforme a documentação
TOKEN_SPECIFICATION = [
    ('COMMENT',       r'#[^\n]*'),              # Comentários
    ('STRING',        r'"[^"]*"'),               # Strings literais
    ('NUMBER',        r'[0-9]+(\.[0-9]+)?'),    # Números (inteiros e ponto flutuante)
    ('KEYWORD',       r'\b(load|filter|select|display|where)\b'), # Palavras-chave
    ('IDENTIFIER',    r'[a-zA-Z_][a-zA-Z0-9_]*'), # Identificadores
    ('OP_ASSIGN',     r'='),                      # Operador de atribuição
    ('OP_REL',        r'==|!=|>=|<=|>|<'),      # Operadores relacionais
    ('LPAREN',        r'\('),                    # Parêntese esquerdo
    ('RPAREN',        r'\)'),                    # Parêntese direito
    ('COMMA',         r','),                      # Vírgula
    ('NEWLINE',       r'\n'),                     # Nova linha (para contar linhas)
    ('WHITESPACE',    r'[ \t]+'),                # Espaço em branco (ignorado)
    ('MISMATCH',      r'.'),                      # Qualquer outro caractere (erro)
]

# Compila as expressões regulares em uma única
TOKEN_REGEX = re.compile('|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION))

def analyze(code):
    tokens = []
    line_num = 1
    line_start = 0

    # Itera sobre todas as correspondências encontradas no código
    for mo in TOKEN_REGEX.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start

        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind in ('WHITESPACE', 'COMMENT'):
            continue
        elif kind == 'MISMATCH':
            # Se um caractere inválido for encontrado, reporta o erro e encerra
            print(f"Erro Léxico: Caractere não reconhecido '{value}' na linha {line_num}, coluna {column + 1}.")
            return None

        tokens.append((value, kind))

    return tokens

def print_token_table(tokens):
    # Determina a largura máxima para cada coluna
    max_token_len = max(len(token) for token, kind in tokens) if tokens else 5
    max_kind_len = max(len(kind) for token, kind in tokens) if tokens else 4

    # Cabeçalho da tabela
    header = f"| {'Token'.ljust(max_token_len)} | {'Tipo'.ljust(max_kind_len)} |"
    separator = f"+-{'-' * max_token_len}-+-{'-' * max_kind_len}-+"

    print(separator)
    print(header)
    print(separator)

    # Corpo da tabela
    for token, kind in tokens:
        print(f"| {token.ljust(max_token_len)} | {kind.ljust(max_kind_len)} |")
    
    print(separator)

if __name__ == '__main__':
    # Garante que o nome do arquivo foi passado como argumento
    if len(sys.argv) != 2:
        print("Uso: python lexer.py <caminho_para_o_arquivo.coffee>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        sys.exit(1)

    # Analisa o código e imprime o resultado
    recognized_tokens = analyze(source_code)
    
    if recognized_tokens:
        print(f"Análise léxica do arquivo '{file_path}' concluída com sucesso:\n")
        print_token_table(recognized_tokens)