# Entrega da Semana 2: Especificação Léxica - Projeto Coffee

Esta entrega detalha a especificação formal do alfabeto e dos tokens da linguagem Coffee, alinhada com os objetivos de ser uma linguagem intuitiva para iniciantes em ciência de dados. As decisões aqui documentadas formam a base para a implementação do analisador léxico (`Strainer`).

-----

## 1\. Especificação Completa do Alfabeto (`Σ`)

O alfabeto da Coffee, denotado por $\\Coffe$, é o conjunto de todos os caracteres válidos que podem ser utilizados para escrever um programa. Para manter a simplicidade e a familiaridade para nosso público-alvo (iniciantes com conhecimento em Python), escolhemos um subconjunto do padrão ASCII.

O alfabeto $\\coffee$ é definido pela união dos seguintes conjuntos de caracteres:

  * **Letras Minúsculas (`letra_min`):**
    `{ a, b, c, ..., z }`
  * **Letras Maiúsculas (`letra_mai`):**
    `{ A, B, C, ..., Z }`
  * **Dígitos (`digito`):**
    `{ 0, 1, 2, ..., 9 }`
  * **Operadores (`op`):**
    `{ =, >, <, !, +,-, *, / }`
  * **Delimitadores (`delim`):**
    `{ (, ), ", ., , }`
  * **Caracteres de Espaçamento (`espaco`):**
    `{ ' ', '\t', '\n', '\r' }` (espaço, tabulação, nova linha, retorno de carro)
  * **Outros Símbolos (`outros`):**
    `{ _, # }` (underscore, cerquilha para comentários)

Formalmente, o alfabeto completo é:
$\\alfabeto\_coffee$ = letra\_min U letra\_mai U digito U op U delim U espaco U outros$

-----

## 2\. Definição Formal dos Tipos de Tokens

Tokens são as unidades léxicas elementares da linguagem, formadas a partir de sequências de caracteres do alfabeto. Usando as operações de linguagens formais, definimos as seguintes classes de tokens para a Coffee.

#### a. Palavras-Chave (Keywords)

Um conjunto finito de palavras com significado reservado.

  * **Linguagem:** $L\_{keywords} = { \\text{load, filter, select, display, where} }$

#### b. Identificadores (Identifiers)

Nomes para variáveis (que armazenarão dados). Devem começar com uma letra ou underscore, seguido por qualquer combinação de letras, dígitos ou underscores.

  * **Conjuntos base:**
      * letra = letra\_min U letra\_mai$
      * inicio\_id = letra U { \_ }$
      * corpo\_id = letra U digito U { \_ }$
  * **Linguagem:** $L\_{id} = inicio\_id \\ (corpo\_id)\*
      * Isso representa a concatenação de um caractere do conjunto `inicio_id` com zero ou mais caracteres (Fechamento de Kleene) do conjunto `corpo_id`.

#### c. Literais (Literals)

Valores de dados fixos.

  * **String:** Uma sequência de quaisquer caracteres entre aspas duplas. Para simplificar, não permitiremos aspas duplas dentro da string.
      * char\_string = $coffee$ - { " }
      * L\_{string} = " (char\_string)^\* "
  * **Número (Inteiro e Ponto Flutuante):**
      * **Inteiro:** Uma sequência de um ou mais dígitos.
          * L\_{int} = (digito)^+
      * **Ponto Flutuante:** Uma sequência de dígitos, um ponto, e outra sequência de dígitos.
          * L\_{float} = (digito)^+ . (digito)^+
      * **Número (geral):** A união das duas linguagens.
          * L\_{num} = L\_{int} \\cup L\_{float}

#### d. Operadores (Operators)

Símbolos para realizar comparações e atribuições.

  * **Operadores de Comparação:**
      * L\_{op\_comp} = { \>, \<, ==, \!=, \>=, \<= }
  * **Operador de Atribuição:**
      * L\_{op\_atrib} = { = }
  * **Operadores (geral):**
      * L\_{op} = L\_{op\_comp} \\cup L\_{op\_atrib}

#### e. Delimitadores (Delimiters)

Símbolos para agrupar e separar elementos.

  * **Linguagem:** $L\_{coffee} = { (, ), . \\ , \\ , }$

#### f. Comentários (Comments)

Texto ignorado pelo compilador. Começa com `#` e vai até o final da linha.

  * char\_comentario = $coffee$ - { '\\n' }
  * L\_{comment} = \\ (char\_comentario)^* \\ ('\\n' \\ | )


-----

## 3\. Exemplos Concretos de Programas Válidos

A seguir, alguns exemplos de código que seriam considerados lexicamente válidos na linguagem Coffee, utilizando os tokens definidos acima.

#### Exemplo 1: Carregar e exibir dados

```coffee
# Carrega os dados de um arquivo CSV em uma variável chamada 'vendas'
vendas = load "dados_de_vendas.csv"

# Mostra as primeiras linhas do conjunto de dados no console
display vendas
```

#### Exemplo 2: Filtrar dados por um critério numérico

```coffee
# Carrega o dataset de produtos
produtos = load "catalogo_produtos.csv"

# Filtra para manter apenas produtos com preço acima de 50.75
produtos_caros = filter produtos where preco > 50.75

# Exibe o resultado da filtragem
display produtos_caros
```

#### Exemplo 3: Selecionar colunas específicas

```coffee
# Carrega dados de clientes
clientes = load "lista_clientes.csv"

# Seleciona apenas as colunas de nome e email para criar uma lista de contatos
lista_contatos = select clientes(nome, email)

display lista_contatos
```

-----

## 4\. Atualização do Diário de Desenvolvimento

**Semana 2 - Decisões de Design Léxico**

  * **Decisão sobre o Alfabeto:** Optamos por um subconjunto do ASCII para o alfabeto inicial da Coffee. A justificativa é manter a linguagem simples e acessível, evitando as complexidades do Unicode nesta fase inicial. Isso garante que qualquer teclado padrão possa ser usado e que o processamento de caracteres seja direto.

  * **Definição de Identificadores:** Adotamos o padrão `(letra | _)(letra | digito | _)*`, comum em linguagens como Python e C. Decidimos que os identificadores serão **case-sensitive** (ex: `Vendas` é diferente de `vendas`). Essa escolha, embora exija mais atenção do programador, é o padrão na maioria das linguagens modernas e ensina uma boa prática de consistência.

  * **Estilo dos Comentários:** Escolhemos o `#` para comentários de linha única. Essa decisão foi fortemente influenciada pelo nosso público-alvo, que provavelmente tem familiaridade com Python, uma linguagem onipresente em ciência de dados. Isso reduz a carga cognitiva e torna o código mais intuitivo para eles.

  * **Literais Numéricos e de String:** Definimos `string` com aspas duplas e números `inteiros` e de `ponto flutuante`. Não incluímos notação científica ou outros formatos numéricos complexos por enquanto, para manter o foco na simplicidade. A prioridade é cobrir os casos de uso mais comuns em análise de dados básica.

  * **Ambiguidade:** Tivemos cuidado para que as definições não gerassem ambiguidades. Por exemplo, um identificador não pode começar com um dígito para não ser confundido com um número. Da mesma forma, as palavras-chave são reservadas e não podem ser usadas como identificadores.