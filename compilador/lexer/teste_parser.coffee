dados = load "arquivo.csv"
dados_filtrados = filter dados where idade > 18
resultado = select dados_filtrados (nome, idade)
display resultado
