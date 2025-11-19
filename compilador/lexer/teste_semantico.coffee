dados = load "vendas.csv"
dados_filtrados = filter dados where preco > 100
resultado = select dados_filtrados (produto, preco, quantidade)
display resultado
