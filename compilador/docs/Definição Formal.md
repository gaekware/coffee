# 💡 Definição Formal da Gramática - Projeto Coffee

Este documento apresenta a gramática formal da linguagem Coffee, inspirada no formato da gramática MicroJava e baseada nas definições estabelecidas nas entregas anteriores do projeto.

A gramática é formalmente definida pela tupla:

**G = (V, Σ, P, S)**

Onde:

  * **V** (Variáveis / Não-Terminais):
    `V = { Program, StatementList, Statement, Assignment, DisplayStatement, FilterStatement, SelectStatement, LogicalExpression, RelationalExpression, Term, LoadInvocation, ColumnList, RelationalOp }`

  * **Σ** (Terminais / Tokens):
    `Σ = { load, filter, select, display, where, identifier, string_literal, number_literal, =, >, <, ==, !=, >=, <=, (, ), ",", ε }`
    *(Nota: `\n` foi omitido pois é tratado como whitespace pelo analisador léxico)*

  * **S** (Símbolo Inicial):
    `S = Program`

  * **P** (Regras de Produção):
    O conjunto de produções segue abaixo, nos formatos EBNF e BNF.

-----

## 📘 Gramática em EBNF (Extended Backus–Naur Form)

```ebnf
Program         = StatementList .
StatementList   = { Statement } .

Statement       = ( Assignment 
                  | DisplayStatement 
                  | FilterStatement 
                  | SelectStatement 
                  ) .

(* --- Sintaxe dos Comandos --- *)

Assignment      = identifier "=" LoadInvocation .
LoadInvocation  = "load" string_literal .

DisplayStatement = "display" identifier .

FilterStatement = identifier "=" "filter" identifier "where" LogicalExpression .

SelectStatement = identifier "=" "select" identifier "(" ColumnList ")" .
ColumnList      = identifier { "," identifier } .

(* --- Estrutura das Expressões --- *)

LogicalExpression  = RelationalExpression .
RelationalExpression = Term RelationalOp Term .
RelationalOp    = ">" | "<" | "==" | "!=" | ">=" | "<=" .
Term            = identifier | number_literal | string_literal .

(* --- Definições Léxicas (Terminais) --- *)
(* Baseado nas Expressões Regulares da Semana 4 *)

identifier     = Letter { Letter | Digit | "_" } .
number_literal = Digit { Digit } [ "." Digit { Digit } ] .
string_literal = '"' { any_char_except_quote } '"' .

Letter         = "a"..."z" | "A"..."Z" | "_" .
Digit          = "0"..."9" .
```

-----

## 📘 Gramática em BNF (Backus-Naur Form)

```bnf
<Program> ::= <StatementList>

<StatementList> ::= <Statement> <StatementList>
                  | ε

<Statement> ::= <Assignment>
              | <DisplayStatement>
              | <FilterStatement>
              | <SelectStatement>

(* --- Sintaxe dos Comandos --- *)

<Assignment> ::= identifier "=" <LoadInvocation>

<LoadInvocation> ::= "load" string_literal

<DisplayStatement> ::= "display" identifier

<FilterStatement> ::= identifier "=" "filter" identifier "where" <LogicalExpression>

<SelectStatement> ::= identifier "=" "select" identifier "(" <ColumnList> ")"

<ColumnList> ::= identifier <ColumnListTail>

<ColumnListTail> ::= "," identifier <ColumnListTail>
                   | ε

(* --- Estrutura das Expressões --- *)

<LogicalExpression> ::= <RelationalExpression>

<RelationalExpression> ::= <Term> <RelationalOp> <Term>

<RelationalOp> ::= ">"
                 | "<"
                 | "=="
                 | "!="
                 | ">="
                 | "<="

<Term> ::= identifier
         | number_literal
         | string_literal
```

-----

## 🧩 Observações

  * **Classificação:** Esta gramática é classificada como **Tipo 2: Gramática Livre de Contexto (GLC)**, conforme justificado na Semana 3.
  * **Análise Sintática:** A gramática está estruturada de forma a ser adequada para um **Analisador Sintático Descendente Recursivo** (*Recursive Descent Parser*), uma decisão tomada na Semana 4.
  * **Listas:**
      * `StatementList` usa recursão à direita, permitindo uma lista de zero ou mais comandos.
      * `ColumnList` (na versão BNF) foi adaptada para um formato padrão de recursão à direita (similar ao `FormPars` do MicroJava) para lidar com listas separadas por vírgula. A versão EBNF (`identifier { "," identifier }`) é equivalente.