#!/bin/bash

# --- Criação da Estrutura Principal ---
echo "Criando diretórios principais..."
mkdir -p compilador/docs/diagramas
mkdir -p compilador/lib/lexer/afds
mkdir -p compilador/lib/lexer/tabelas
mkdir -p compilador/lib/parser/ast
mkdir -p compilador/lib/parser/descendente
mkdir -p compilador/lib/parser/ascendente
mkdir -p compilador/lib/semantic
mkdir -p compilador/lib/codegen
mkdir -p compilador/lib/utils
mkdir -p compilador/test/lexer_test
mkdir -p compilador/test/parser_test
mkdir -p compilador/test/semantic_test
mkdir -p compilador/test/integration_test
mkdir -p compilador/test/fixtures/programas_validos
mkdir -p compilador/test/fixtures/programas_com_erro
mkdir -p compilador/examples/basicos
mkdir -p compilador/examples/intermediarios
mkdir -p compilador/examples/avancados
mkdir -p compilador/tools
mkdir -p compilador/scripts

# --- Criação dos Arquivos ---
echo "Criando arquivos vazios..."

# Raiz
touch compilador/README.md
touch compilador/.gitignore

# Documentação
touch compilador/docs/arquitetura.md
touch compilador/docs/guia-desenvolvimento.md
touch compilador/docs/especificacao-linguagem.md

# Diagramas
touch compilador/docs/diagramas/afd-identificador.md
touch compilador/docs/diagramas/afd-numero.md
touch compilador/docs/diagramas/fluxo-analise-lexica.md

# Lib (Código Fonte)
touch compilador/lib/compilador.py

# Análise Léxica
touch compilador/lib/lexer/lexer.py
touch compilador/lib/lexer/afd_base.py
touch compilador/lib/lexer/token.py
touch compilador/lib/lexer/analisador_lexico.py
touch compilador/lib/lexer/afds/afd_identificador.py
touch compilador/lib/lexer/afds/afd_numero.py
touch compilador/lib/lexer/afds/afd_operador.py
touch compilador/lib/lexer/tabelas/tabela_palavras_chave.py
touch compilador/lib/lexer/tabelas/tabela_operadores.py

# Análise Sintática
touch compilador/lib/parser/parser.py
touch compilador/lib/parser/ast/ast_base.py
touch compilador/lib/parser/ast/expressoes.py
touch compilador/lib/parser/ast/declaracoes.py
touch compilador/lib/parser/descendente/parser_ll1.py
touch compilador/lib/parser/descendente/tabela_parsing.py
touch compilador/lib/parser/ascendente/parser_lr.py

# Análise Semântica
touch compilador/lib/semantic/semantic.py
touch compilador/lib/semantic/tabela_simbolos.py
touch compilador/lib/semantic/verificador_tipos.py
touch compilador/lib/semantic/analisador_semantico.py

# Geração de Código
touch compilador/lib/codegen/codegen.py
touch compilador/lib/codegen/gerador_codigo.py
touch compilador/lib/codegen/otimizador.py

# Utilitários
touch compilador/lib/utils/erro_handler.py
touch compilador/lib/utils/source_location.py
touch compilador/lib/utils/debug_utils.py

# Testes
touch compilador/test/lexer_test/afd_identificador_test.py
touch compilador/test/lexer_test/afd_numero_test.py
touch compilador/test/lexer_test/tabela_palavras_chave_test.py
touch compilador/test/lexer_test/analisador_lexico_test.py
touch compilador/test/parser_test/parser_ll1_test.py
touch compilador/test/parser_test/ast_test.py
touch compilador/test/semantic_test/tabela_simbolos_test.py
touch compilador/test/semantic_test/verificador_tipos_test.py
touch compilador/test/integration_test/compilador_completo_test.py
touch compilador/test/integration_test/programas_exemplo_test.py

# Arquivos de Teste (Fixtures)
touch compilador/test/fixtures/programas_validos/hello_world.dg
touch compilador/test/fixtures/programas_validos/calculadora.dg
touch compilador/test/fixtures/programas_validos/fibonacci.dg
touch compilador/test/fixtures/programas_com_erro/erro_lexico.dg
touch compilador/test/fixtures/programas_com_erro/erro_sintatico.dg
touch compilador/test/fixtures/programas_com_erro/erro_semantico.dg

# Exemplos
touch compilador/examples/basicos/variaveis.dg
touch compilador/examples/basicos/funcoes.dg
touch compilador/examples/basicos/condicionais.dg
touch compilador/examples/intermediarios/classes.dg
touch compilador/examples/intermediarios/heranca.dg
touch compilador/examples/intermediarios/arquitetura_mvc.dg
touch compilador/examples/avancados/sistema_bancario.dg
touch compilador/examples/avancados/jogo_da_velha.dg
touch compilador/examples/avancados/web_service.dg

# Ferramentas
touch compilador/tools/gerador_tabelas.py
touch compilador/tools/validador_gramatica.py
touch compilador/tools/formatter_didatica.py

# Scripts
touch compilador/scripts/run_all_tests.sh
touch compilador/scripts/generate_docs.sh
touch compilador/scripts/build_release.sh

echo "Estrutura para projeto Python criada com sucesso!"