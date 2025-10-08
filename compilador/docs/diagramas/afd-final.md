# Diagrama do Autômato Finito Determinístico (AFD) - Linguagem Coffee

stateDiagram-v2
    direction LR

    [*] --> S0

    %% Estado Inicial e transições primárias
    S0 --> S1_ID: letra, _
    S0 --> S2_NUM: dígito
    S0 --> S4_GT: >
    S0 --> S5_LT: <
    S0 --> S6_EQ: =
    S0 --> S7_NE: !
    S0 --> S8_STR: "
    S0 --> S9_LPAREN: (
    S0 --> S10_RPAREN: )
    S0 --> S11_COMMA: ,
    S0 --> S12_COMMENT: #

    %% Caminho para Identificadores e Palavras-Chave
    state "S1_ID ((ID/KW))" as S1_ID
    S1_ID --> S1_ID: letra, dígito, _
    note right of S1_ID
      Estado de aceitação para Identificadores.
      Após reconhecer, uma tabela de símbolos
      verifica se é uma Palavra-Chave (KW).
    end note

    %% Caminho para Números (Inteiros e Ponto Flutuante)
    state "S2_NUM ((NUMBER))" as S2_NUM
    S2_NUM --> S2_NUM: dígito
    S2_NUM --> S3_FLOAT: .

    state "S3_FLOAT_NUM ((NUMBER))" as S3_FLOAT_NUM
    S3_FLOAT --> S3_FLOAT_NUM: dígito
    S3_FLOAT_NUM --> S3_FLOAT_NUM: dígito

    %% Caminho para Operadores Relacionais Compostos
    state "S4_GT ((OP_REL))" as S4_GT
    S4_GT --> S4_GE: =
    state "S4_GE ((OP_REL))" as S4_GE

    state "S5_LT ((OP_REL))" as S5_LT
    S5_LT --> S5_LE: =
    state "S5_LE ((OP_REL))" as S5_LE

    state "S6_EQ ((OP_ASSIGN))" as S6_EQ
    S6_EQ --> S6_EQEQ: =
    state "S6_EQEQ ((OP_REL))" as S6_EQEQ

    S7_NE --> S7_NE_EQ: =
    state "S7_NE_EQ ((OP_REL))" as S7_NE_EQ

    %% Caminho para Strings, Delimitadores e Comentários
    state "S8_STR" as S8_STR
    S8_STR --> S8_STR: qualquer_char exceto "
    S8_STR --> S8_END_STR: "
    state "S8_END_STR ((STRING))" as S8_END_STR

    state "S9_LPAREN ((LPAREN))" as S9_LPAREN
    state "S10_RPAREN ((RPAREN))" as S10_RPAREN
    state "S11_COMMA ((COMMA))" as S11_COMMA

    state "S12_COMMENT" as S12_COMMENT
    S12_COMMENT --> S12_COMMENT: qualquer_char exceto \n
    note right of S12_COMMENT
      Comentários são reconhecidos mas
      descartados pelo analisador.
    end note