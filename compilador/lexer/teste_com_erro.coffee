# Arquivo para testar o tratamento de erros léxicos

# Carrega os dados de um arquivo CSV
vendas = load "dados_de_vendas.csv"

# Erro: O símbolo '$' não é um caractere válido na linguagem Coffee
total_lucro = vendas$total * 0.2

display total_lucro