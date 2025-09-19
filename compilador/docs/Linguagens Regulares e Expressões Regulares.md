# Entrega da Semana 4: Linguagens Regulares e Expressões Regulares - Projeto Coffee

Este documento reformula a especificação léxica da linguagem Coffee utilizando expressões regulares, analisa ambiguidades e define uma estratégia para o tratamento de erros léxicos. O objetivo é preparar a base para a implementação do analisador léxico (`Strainer`).

-----

## 1\. Especificação Completa Usando Expressões Regulares

A seguir, cada tipo de token da linguagem Coffee é formalmente definido por meio de uma expressão regular. Essas definições são a base para o analisador léxico reconhecer as unidades fundamentais do código-fonte.

#### **a. Palavras-Chave (Keywords)**

As palavras-chave são literais de texto fixos e reservados.

  * `load`
  * `filter`
  * `select`
  * `display`
  * `where`

#### **b. Identificadores (Identifiers)**

Nomes definidos pelo usuário para variáveis. Devem começar com uma letra ou underscore, seguidos por letras, números ou underscores.

  * **Expressão Regular:** `[a-zA-Z_][a-zA-Z0-9_]*`
  * **Exemplos:** `raw_data`, `_vendas`, `produtos_caros`, `lista1`

#### **c. Literais (Literals)**

Valores de dados fixos no código.

  * **String:** Uma sequência de quaisquer caracteres, exceto aspas duplas, delimitada por aspas duplas.
      * **Expressão Regular:** `"[^"]*"`
      * **Exemplos:** `"sales.csv"`, `"lista_clientes.csv"`
  * **Número (Number):** Inclui números inteiros e de ponto flutuante.
      * **Expressão Regular:** `[0-9]+(\.[0-9]+)?`
      * **Explicação:** Uma sequência de um ou mais dígitos, opcionalmente seguida por um ponto e outra sequência de um ou mais dígitos.
      * **Exemplos:** `100`, `50.75`, `10`

#### **d. Operadores (Operators)**

Símbolos que representam operações de atribuição e comparação.

  * **Atribuição (`=`):** `=`
  * **Comparação (`>`, `<`, `==`, `!=`, `>=`, `<=`):** `> | < | == | != | >= | <=`

#### **e. Delimitadores (Delimiters)**

Símbolos usados para agrupar e separar elementos sintáticos.

  * **Parênteses:** `\( | \)`
  * **Vírgula:** `,`

#### **f. Comentários (Comments)**

Texto que deve ser ignorado pelo compilador. Começa com `#` e vai até o final da linha.

  * **Expressão Regular:** `#[^\n]*`
  * **Exemplo:** `# Carrega os dados de um arquivo`

#### **g. Espaços em Branco (Whitespace)**

Caracteres de espaçamento que são ignorados pelo analisador léxico, mas que servem para separar tokens.

  * **Expressão Regular:** `[ \t\r\n]+`
  * **Nota:** Embora ignorado, o caractere de nova linha (`\n`) pode ser usado para determinar o número das linhas, o que é crucial para reportar erros.

-----

## 2\. Análise de Ambiguidade e Regras de Resolução

A principal fonte de ambiguidade léxica em Coffee ocorre entre **Palavras-Chave** e **Identificadores**. Por exemplo, a sequência de caracteres `filter` corresponde tanto à expressão regular para identificadores (`[a-zA-Z_][a-zA-Z0-9_]*`) quanto à palavra-chave `filter`.

Para resolver essa sobreposição, estabelecemos uma regra de precedência clara:

  * **Regra de Precedência (Princípio da Correspondência Máxima):** O analisador léxico deve sempre favorecer a correspondência mais específica. Ao encontrar uma sequência de caracteres que se encaixa tanto como palavra-chave quanto como identificador, ela **deve ser classificada como Palavra-Chave**.

**Implementação Prática:**

1.  O analisador léxico primeiro tenta corresponder a sequência a uma das palavras-chave da lista (`load`, `filter`, etc.).
2.  Se, e somente se, nenhuma correspondência for encontrada na lista de palavras-chave, a sequência será então testada contra a expressão regular de identificadores.

Essa abordagem garante que os nomes reservados da linguagem não possam ser usados como nomes de variáveis, evitando conflitos sintáticos.

-----

## 3\. Estratégia para Tratamento de Erros Léxicos

Quando o analisador léxico (`Strainer`) encontra uma sequência de caracteres que não corresponde a nenhum token definido, um erro léxico ocorre. Nossa estratégia para lidar com esses erros focará em fornecer feedback claro ao usuário sem interromper completamente a análise, permitindo a identificação de múltiplos erros em uma única compilação.

**Estratégia de Recuperação (Modo Pânico Simples):**

1.  **Detecção:** Ao encontrar um caractere inválido (que não pode iniciar nenhum token válido), o analisador registra um erro.
2.  **Registro do Erro:** O erro é registrado com as seguintes informações:
      * A mensagem de erro descritiva.
      * O caractere ou a sequência de caracteres inválida.
      * O número da linha e da coluna onde o erro ocorreu.
3.  **Sincronização:** Após registrar o erro, o analisador entra em "modo de recuperação". Ele descarta os caracteres subsequentes da entrada até encontrar um caractere que possa iniciar um novo token de forma confiável (como um espaço em branco, uma nova linha ou o início de um token conhecido como `"` ou uma letra).
4.  **Continuação:** Uma vez sincronizado, o analisador retoma a análise léxica normal a partir do novo ponto.

Essa abordagem evita que um único erro léxico gere uma cascata de erros sintáticos falsos e permite que o usuário receba um relatório mais completo dos problemas em seu código.

-----

## 4\. Esboços de Mensagens de Erro para Usuários

As mensagens de erro são projetadas para serem claras e úteis para nosso público-alvo: iniciantes em ciência de dados. Elas indicarão o problema, a localização e, quando possível, uma sugestão de correção.

#### **Erro 1: Caractere Inválido**

  * **Cenário:** O usuário digita um caractere que não pertence ao alfabeto da linguagem.
    ```coffee
    # Tenta filtrar usando um operador inválido
    dados_filtrados = filter dados_brutos where valor @ 100 
    ```
  * **Mensagem de Erro:**
    ```
    Erro Léxico: Caractere inesperado.
    --> Linha 2, Coluna 48
    |
    2 | dados_filtrados = filter dados_brutos where valor @ 100
    |                                                ^
    = Ajuda: O símbolo '@' não é um operador válido em Coffee. Você quis dizer '==' ou '>='?
    ```

#### **Erro 2: String Não Fechada**

  * **Cenário:** O usuário esquece de fechar as aspas de uma string literal.
    ```coffee
    meus_dados = load "dados.csv
    ```
  * **Mensagem de Erro:**
    ```
    Erro Léxico: String não foi fechada.
    --> Linha 1, Coluna 19
    |
    1 | meus_dados = load "dados.csv
    |                   ^
    = Ajuda: Literais de texto (strings) devem começar e terminar com aspas duplas (").
    ```

#### **Erro 3: Número Malformado**

  * **Cenário:** O usuário digita um número com múltiplos pontos decimais.
    ```coffee
    limite = 50.75.2
    ```
  * **Mensagem de Erro:**
    ```
    Erro Léxico: Número com formato inválido.
    --> Linha 1, Coluna 10
    |
    1 | limite = 50.75.2
    |          ^
    = Ajuda: Um número pode conter no máximo um ponto decimal.
    ```

## 5. Atualização do Diário de Desenvolvimento

**Semana 4 - Análise Sintática e Estrutura da AST**

* **Resumo da Semana:** O foco desta semana foi a transição da análise léxica para a análise sintática. Com os tokens definidos, o próximo passo foi construir um *parser* capaz de validar a estrutura do código Coffee com base na gramática formal. O principal resultado deste processo é a geração de uma Árvore Sintática Abstrata (AST), que servirá de base para a futura análise semântica.

* **Decisões Tomadas:**
    * **Escolha do Algoritmo de Parsing:** Optamos por implementar um **Analisador Sintático Descendente Recursivo** (*Recursive Descent Parser*). Esta abordagem foi escolhida por sua simplicidade e correspondência direta com a nossa Gramática Livre de Contexto (GLC). Cada variável (símbolo não-terminal) da gramática, como `Statement` ou `Assignment`, foi mapeada para uma função no código do parser.
    * **Estrutura da Árvore Sintática Abstrata (AST):** Definimos uma estrutura de nós para a AST que representa fielmente os comandos da linguagem. Por exemplo:
        * Um comando `vendas = load "dados.csv"` é transformado em um `AssignmentNode`.
        * Este nó contém o identificador (`vendas`) e um `LoadInvocationNode`.
        * O `LoadInvocationNode`, por sua vez, armazena o literal de string (`"dados.csv"`).
    * **Tratamento de Erros Sintáticos:** Adotamos uma estratégia de "modo pânico" para a recuperação de erros. Quando o parser encontra um token inesperado (ex: `load` sem uma string em seguida), ele reporta um erro claro indicando o que era esperado e o que foi encontrado. Em seguida, ele descarta os tokens até encontrar o início de um novo comando (como `display`, `filter`, etc.), permitindo que a análise continue e múltiplos erros sejam reportados de uma só vez.

* **Desafios Encontrados:**
    * O principal desafio foi garantir que a recursão na regra `StatementList -> Statement StatementList` fosse tratada corretamente para ler programas com múltiplos comandos sequenciais.
    * Mapear a estrutura da cláusula `where`, definida como `Term RelationalOp Term`, para um nó de expressão na AST exigiu um cuidado especial para capturar corretamente o operador e os dois operandos (termos).

* **Observações Adicionais:**
    * A implementação do parser reforçou a importância de uma gramática bem definida e não ambígua. A clareza da gramática da Semana 3 facilitou significativamente a codificação do analisador sintático.
    * A AST criada agora forma a espinha dorsal do compilador, e as próximas etapas dependerão diretamente de sua estrutura.