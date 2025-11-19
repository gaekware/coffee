dados_vendas = load "vendas_2025.csv"
dados_produtos = load "produtos.json"

vendas_filtradas = filter dados_vendas where quantidade >= 10
produtos_ativos = filter dados_produtos where status == "ativo"

relatorio_vendas = select vendas_filtradas (produto, quantidade, valor_total)
catalogo = select produtos_ativos (nome, categoria, preco)

display relatorio_vendas
display catalogo
