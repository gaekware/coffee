# Entrega da Semana 3: Gramática Formal - Projeto Coffee

Este documento apresenta a primeira versão da gramática formal para a linguagem **Coffee**.  
O objetivo é definir a estrutura sintática da linguagem, estabelecer sua classificação na hierarquia de **Chomsky** e analisar potenciais ambiguidades.  

---

## 1. Primeira Versão da Gramática Formal  

A gramática da Coffee é formalmente definida pela tupla:  

VTPS:
- **V:** Conjunto de símbolos não-terminais (variáveis).  
- **T:** Conjunto de símbolos terminais (tokens).  
- **P:** Regras de produção.  
- **S:** Símbolo inicial.

### Definição Completa `G = (V, T, P, S)`  

#### Conjunto de Variáveis (V)  
```

V = { Program, StatementList, Statement, Assignment,
DisplayStatement, FilterStatement, SelectStatement,
LogicalExpression, RelationalExpression, Term, LoadInvocation,
ColumnList, RelationalOp }

```

#### Conjunto de Terminais (T)  
```

T = { load, filter, select, display, where, identifier,
string\_literal, number\_literal, =, >, <, ==, !=, >=, <=,
(, ), ",", \n, ε }

```

#### Símbolo Inicial (S)  
```

S = Program

```

---

### Regras de Produção (P)  

As regras a seguir foram projetadas para serem simples, expressivas e alinhadas ao paradigma imperativo e de domínio específico da Coffee.  

#### Estrutura do Programa  
```

Program -> StatementList
StatementList -> Statement StatementList | ε

```
> Um programa é uma sequência de comandos.  
> A recursão à direita permite uma lista de qualquer tamanho.  

#### Tipos de Comandos  
```

Statement -> Assignment | DisplayStatement | FilterStatement | SelectStatement

```
> Define as quatro operações fundamentais da linguagem na sua versão inicial.  

#### Sintaxe dos Comandos  

**Atribuição**
```

Assignment -> identifier = LoadInvocation
LoadInvocation -> load string\_literal

````
Exemplo:  
```coffee
raw_data = load "sales.csv"
````

**Exibição**

```
DisplayStatement -> display identifier
```

Exemplo:

```coffee
display raw_data
```

**Filtragem**

```
FilterStatement -> identifier = filter identifier where LogicalExpression
```

Exemplo:

```coffee
high_sales = filter raw_data where value > 100
```

**Seleção**

```
SelectStatement -> identifier = select identifier ( ColumnList )
ColumnList -> identifier , ColumnList | identifier
```

Exemplo:

```coffee
contacts = select customers (name, email)
```

---

### Estrutura das Expressões (cláusula `where`)

```
LogicalExpression -> RelationalExpression
RelationalExpression -> Term RelationalOp Term
RelationalOp -> > | < | == | != | >= | <=
Term -> identifier | number_literal | string_literal
```

Exemplo:

```coffee
price >= 50.75
```

Um **Term** pode ser o nome de uma coluna, um número ou um texto.

---

## 2. Classificação na Hierarquia de Chomsky

A gramática desenvolvida para a Coffee é classificada como **Tipo 2: Gramática Livre de Contexto (GLC)**.

### Justificativa

* **Formato das Regras:** Todas seguem o formato `A → α`, onde `A` é um único não-terminal.
* **Insuficiência das Gramáticas Regulares (Tipo 3):** Necessidade de recursão (ex: `StatementList`).
* **Desnecessidade das Gramáticas Sensíveis ao Contexto (Tipo 1):** As regras independem do contexto, restrições semânticas serão tratadas depois.
* **Equilíbrio:** GLC garante expressividade e simplicidade, permitindo parsers eficientes.

---

## 3. Exemplos de Derivações

### Derivação 1: Comando de Carga de Dados

**Código:**

```coffee
sales = load "data.csv"
```

**Derivação:**

```
Program
=> StatementList
=> Statement ε
=> Assignment
=> identifier = LoadInvocation
=> sales = LoadInvocation
=> sales = load string_literal
=> sales = load "data.csv"
```

---

### Derivação 2: Comando de Filtragem

**Código:**

```coffee
vip_customers = filter customers where purchases > 10
```

**Derivação:**

```
Program
=> StatementList
=> Statement ε
=> FilterStatement
=> identifier = filter identifier where LogicalExpression
=> vip_customers = filter customers where LogicalExpression
=> vip_customers = filter customers where RelationalExpression
=> vip_customers = filter customers where Term RelationalOp Term
=> vip_customers = filter customers where identifier RelationalOp Term
=> vip_customers = filter customers where purchases RelationalOp Term
=> vip_customers = filter customers where purchases > Term
=> vip_customers = filter customers where purchases > number_literal
=> vip_customers = filter customers where purchases > 10
```

---

## 4. Análise de Ambiguidades Potenciais e Estratégias de Resolução

### Problema: Precedência de Operadores

Se fossem adicionadas expressões aritméticas:

```
Expression -> Expression + Expression | Expression * Expression | number
```

A sentença `3 + 5 * 2` poderia ser ambígua.

**Solução:** Hierarquia de não-terminais para impor precedência.

Exemplo:

```
LogicalExpression -> LogicalExpression AND RelationalExpression | RelationalExpression
```

Isso força `RelationalExpression` a ser avaliada antes de `AND`.

---

### Problema: Associatividade de Operadores

* **Associatividade à Esquerda** (padrão `+ - * /`):

```
Expression -> Expression + Term | Term
```

* **Associatividade à Direita** (atribuição `=`):

```
Assignment -> identifier = Assignment | Expression
```

### Controle da Ordem pelo Usuário

Uso de parênteses:

```
Term -> ... | ( LogicalExpression )
```

---

✅ Com essas estratégias, a gramática Coffee se mantém **não ambígua** e **expansível** para futuras funcionalidades.

```

Quer que eu também faça um **sumário automático (table of contents)** no início para facilitar a navegação do documento em Markdown?
```
