# Analisador Léxico para a Linguagem Coffee (Strainer)

Este diretório contém a implementação do analisador léxico para a linguagem de programação Coffee. O analisador, apelidado de `Strainer` (o "filtro"), é responsável por ler um arquivo de código-fonte `.coffee` e dividi-lo em uma sequência de tokens.

O script `lexer.py` foi projetado para identificar todas as unidades léxicas definidas na especificação da linguagem, como palavras-chave, identificadores, literais, operadores e delimitadores.

## Requisitos

- Python 3.x

Não há necessidade de instalar bibliotecas externas.

## Como Executar o Analisador

O analisador é executado através da linha de comando, passando o caminho do arquivo `.coffee` que você deseja analisar como argumento.

1.  **Navegue até o diretório `lexer` pelo seu terminal.**

2.  **Execute o script usando o seguinte comando:**
    ```sh
    python lexer.py <caminho_para_o_arquivo.coffee>
    ```

### Exemplo de Uso com um Código Válido

Para analisar o arquivo `index.coffee` incluído neste diretório, execute:

```sh
python lexer.py index.coffee