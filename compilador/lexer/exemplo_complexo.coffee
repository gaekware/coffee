vendas_janeiro = load "vendas_jan_2025.csv"
vendas_fevereiro = load "vendas_fev_2025.csv"

clientes_vip = load "clientes_premium.json"

vendas_altas_jan = filter vendas_janeiro where total >= 1000
vendas_altas_fev = filter vendas_fevereiro where total >= 1000

produtos_populares_jan = select vendas_altas_jan (produto, quantidade, total)
produtos_populares_fev = select vendas_altas_fev (produto, quantidade, total)

clientes_jovens = filter clientes_vip where idade <= 35
contatos_marketing = select clientes_jovens (nome, email, cidade)

display produtos_populares_jan
display produtos_populares_fev
display contatos_marketing