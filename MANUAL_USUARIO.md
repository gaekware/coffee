# Manual de Utilização - Compilador Coffee

## Visão Geral

O Compilador Coffee é um sistema completo para processamento de dados usando uma linguagem de domínio específico (DSL) projetada para análise de datasets. Este manual ensina como usar o compilador para escrever e executar programas Coffee.

## 1. Linguagem Coffee

### 1.1 Conceitos Básicos

A linguagem Coffee é focada em manipulação de dados tabulares (datasets) usando operações simples e intuitivas:

- **Load**: Carrega dados de arquivos CSV ou JSON
- **Filter**: Filtra linhas baseado em condições
- **Select**: Seleciona colunas específicas
- **Display**: Exibe resultados formatados

### 1.2 Sintaxe Básica

#### Declaração de Variáveis
```coffee
nome_variavel = operacao
```

#### Operações Disponíveis

**1. Load (Carregar Dados)**
```coffee
dados = load "arquivo.csv"
dados_json = load "dados.json"
```

**2. Filter (Filtrar Linhas)**
```coffee
filtrados = filter dados where coluna > 100
filtrados = filter dados where nome == "João"
filtrados = filter dados where idade >= 18
```

**3. Select (Selecionar Colunas)**
```coffee
resultado = select dados (coluna1, coluna2, coluna3)
contatos = select clientes (nome, email)
```

**4. Display (Exibir Resultados)**
```coffee
display dados
display resultado
```

### 1.3 Tipos de Dados

- **Dataset**: Conjunto de dados tabulares (como uma planilha)
- **String**: Texto entre aspas duplas ("exemplo")
- **Number**: Números inteiros ou decimais (100, 3.14)
- **Boolean**: Valores verdadeiro/falso
- **Column**: Referência a uma coluna de dataset

### 1.4 Operadores de Comparação

- `>` : Maior que
- `<` : Menor que
- `>=`: Maior ou igual
- `<=`: Menor ou igual
- `==`: Igual
- `!=`: Diferente

## 2. Usando o Compilador

### 2.1 Estrutura de um Programa Coffee

```coffee
# Carrega dados de vendas
vendas = load "vendas.csv"

# Filtra vendas acima de R$ 1000
vendas_altas = filter vendas where valor > 1000

# Seleciona apenas produto e valor
relatorio = select vendas_altas (produto, valor)

# Exibe o resultado
display relatorio
```

### 2.2 Executando Programas

**Usando o Interpretador (Recomendado):**
```bash
python coffee_interpreter.py meu_programa.coffee
```

**Usando apenas o Parser (para verificar sintaxe):**
```bash
python parser.py meu_programa.coffee
```

**Usando o Analisador Semântico:**
```bash
python semantic_analyzer.py meu_programa.coffee
```

### 2.3 Formatos de Arquivo Suportados

**CSV (Comma-Separated Values):**
```csv
nome,idade,cidade
João,25,São Paulo
Maria,30,Rio de Janeiro
Pedro,28,Belo Horizonte
```

**JSON (JavaScript Object Notation):**
```json
[
  {"nome": "João", "idade": 25, "cidade": "São Paulo"},
  {"nome": "Maria", "idade": 30, "cidade": "Rio de Janeiro"},
  {"nome": "Pedro", "idade": 28, "cidade": "Belo Horizonte"}
]
```

## 3. Exemplos Práticos

### 3.1 Análise de Vendas

```coffee
# Carrega dados de vendas do mês
vendas_marco = load "vendas_marco_2025.csv"

# Filtra vendas do produto "Notebook"
vendas_notebook = filter vendas_marco where produto == "Notebook"

# Seleciona informações relevantes
relatorio_notebook = select vendas_notebook (data, quantidade, valor_total)

# Exibe o relatório
display relatorio_notebook
```

### 3.2 Gestão de Clientes

```coffee
# Carrega base de clientes
clientes = load "clientes.csv"

# Filtra clientes jovens (até 30 anos)
clientes_jovens = filter clientes where idade <= 30

# Seleciona dados para campanha de marketing
campanha = select clientes_jovens (nome, email, telefone)

# Mostra os contatos
display campanha
```

### 3.3 Análise de Produtos

```coffee
# Carrega catálogo de produtos
produtos = load "catalogo.json"

# Filtra produtos ativos
produtos_ativos = filter produtos where status == "ativo"

# Filtra produtos caros
produtos_premium = filter produtos_ativos where preco >= 1000

# Seleciona informações do relatório
relatorio = select produtos_premium (nome, categoria, preco)

# Exibe produtos premium
display relatorio
```

## 4. Tratamento de Erros

### 4.1 Erros Comuns

**1. Arquivo não encontrado:**
```
Erro: Arquivo 'dados.csv' não encontrado
```
*Solução:* Verifique se o arquivo existe e o caminho está correto.

**2. Coluna inexistente:**
```
Erro: Coluna 'preço' não existe. Colunas disponíveis: nome, preco, quantidade
```
*Solução:* Verifique o nome correto da coluna (note o erro de grafia).

**3. Variável não declarada:**
```
Erro: Variável 'dados' não foi declarada
```
*Solução:* Declare a variável antes de usá-la.

**4. Tipo incompatível:**
```
Erro: Display só pode ser usado com datasets
```
*Solução:* Use display apenas com variáveis do tipo dataset.

### 4.2 Mensagens de Sucesso

Quando tudo funciona corretamente:
```
============================================================
DATASET: relatorio
============================================================
Linhas: 15 | Colunas: 3
Colunas: produto, quantidade, valor
------------------------------------------------------------
   produto  quantidade    valor
  Notebook           5  12500.0
     Mouse          20    800.0
   Teclado          10   1500.0
...
============================================================

Programa executado com sucesso!
```

## 5. Dicas e Boas Práticas

### 5.1 Nomenclatura

- Use nomes descritivos para variáveis: `vendas_janeiro` em vez de `v1`
- Use snake_case: `dados_filtrados` em vez de `dadosFiltrados`
- Seja consistente com a nomenclatura

### 5.2 Organização do Código

```coffee
# 1. Carregamento de dados
vendas = load "vendas.csv"
clientes = load "clientes.csv"

# 2. Processamento
vendas_altas = filter vendas where valor > 1000
clientes_vip = filter clientes where categoria == "VIP"

# 3. Seleção de dados
relatorio = select vendas_altas (produto, valor, cliente)
contatos = select clientes_vip (nome, email)

# 4. Exibição de resultados
display relatorio
display contatos
```

### 5.3 Performance

- Filtre dados antes de fazer seleções para reduzir processamento
- Use nomes de coluna exatos para evitar erros
- Carregue apenas os arquivos necessários

## 6. Recursos Avançados

### 6.1 Múltiplos Filtros

```coffee
dados = load "funcionarios.csv"

# Filtro combinado: funcionários jovens com salário alto
funcionarios_selecionados = filter dados where idade < 30
funcionarios_bem_pagos = filter funcionarios_selecionados where salario > 5000

display funcionarios_bem_pagos
```

### 6.2 Análise Comparativa

```coffee
vendas_2024 = load "vendas_2024.csv"
vendas_2025 = load "vendas_2025.csv"

produtos_2024 = select vendas_2024 (produto, total)
produtos_2025 = select vendas_2025 (produto, total)

display produtos_2024
display produtos_2025
```

## 7. Solução de Problemas

### 7.1 Verificando a Sintaxe

Se não tem certeza se seu código está correto, use o parser:
```bash
python parser.py meu_programa.coffee
```

### 7.2 Verificando a Semântica

Para verificar se as variáveis e tipos estão corretos:
```bash
python semantic_analyzer.py meu_programa.coffee
```

### 7.3 Executando com Debug

Para ver informações detalhadas durante a execução, edite o arquivo e mude `debug=False` para `debug=True`.

## 8. Referência Rápida

### 8.1 Comandos Essenciais

| Operação | Sintaxe | Exemplo |
|----------|---------|---------|
| Carregar | `var = load "arquivo"` | `dados = load "vendas.csv"` |
| Filtrar | `var = filter dataset where condição` | `filtrados = filter dados where idade > 18` |
| Selecionar | `var = select dataset (cols)` | `resultado = select dados (nome, idade)` |
| Exibir | `display variavel` | `display resultado` |

### 8.2 Operadores

| Operador | Descrição | Exemplo |
|----------|-----------|---------|
| `>` | Maior que | `preco > 100` |
| `<` | Menor que | `idade < 30` |
| `>=` | Maior ou igual | `nota >= 7` |
| `<=` | Menor ou igual | `desconto <= 0.1` |
| `==` | Igual | `status == "ativo"` |
| `!=` | Diferente | `tipo != "teste"` |

---

**Suporte:** Para dúvidas ou problemas, consulte a documentação técnica ou execute os testes incluídos no projeto.