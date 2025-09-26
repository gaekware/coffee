# 1. Carrega dados de vendas e clientes
vendas_2025 = load "dados_vendas.csv"
clientes_vip = load "clientes.csv"

# 2. Mostra o conteúdo inicial da variável 'vendas_2025'
display vendas_2025

# 3. Filtra vendas para encontrar transações de alto valor
vendas_altas = filter vendas_2025 where total > 500.75

# 4. Seleciona colunas específicas dos clientes para criar uma lista de contatos
contatos = select clientes_vip (nome, email)

# 5. Exibe o resultado final
display contatos