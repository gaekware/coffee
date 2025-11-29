# Manual de Instalação - Compilador Coffee

## Guia Completo para Iniciantes

Este manual ensina como instalar e configurar o Compilador Coffee do zero, assumindo que você nunca programou antes. Siga todos os passos na ordem apresentada.

## 1. Pré-requisitos do Sistema

### 1.1 Sistemas Operacionais Suportados
- Windows 10/11 (todas as edições)
- macOS 10.14 ou superior
- Linux (Ubuntu 18.04+, Fedora 30+, outras distribuições modernas)

### 1.2 Verificando seu Sistema

**Windows:**
1. Clique em "Iniciar" → "Configurações" → "Sistema" → "Sobre"
2. Verifique se tem Windows 10 ou 11

**macOS:**
1. Clique no menu Apple → "Sobre este Mac"
2. Verifique se tem macOS 10.14 ou superior

**Linux:**
1. Abra o terminal (Ctrl+Alt+T)
2. Digite: `lsb_release -a`

## 2. Instalação do Python

### 2.1 Windows

**Passo 1: Baixar Python**
1. Acesse: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Clique em "Download Python 3.11.x" (versão mais recente)
3. Execute o arquivo baixado

**Passo 2: Instalar Python**
1. **ATENÇÃO ESPECIAL**: Certifique-se de marcar a opção "Add Python to PATH"
2. Clique em "Install Now"
3. Aguarde a instalação
4. Clique em "Close"

**Passo 3: Verificar Instalação**
1. Pressione `Windows + R`
2. Digite `cmd` e pressione Enter
3. No terminal, digite exatamente: `python --version`
4. Se a instalação foi bem-sucedida, deve aparecer algo como: `Python 3.11.x`

### 2.2 macOS

**Passo 1: Instalar Homebrew (Gerenciador de Pacotes)**
1. Abra o Terminal (Cmd+Space, digite "Terminal")
2. Cole este comando e pressione Enter:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
3. Digite sua senha quando solicitado
4. Aguarde a instalação

**Passo 2: Instalar Python**
```bash
brew install python
```

**Passo 3: Verificar Instalação**
```bash
python3 --version
```

### 2.3 Linux (Ubuntu/Debian)

**Passo 1: Atualizar Sistema**
```bash
sudo apt update
sudo apt upgrade
```

**Passo 2: Instalar Python**
```bash
sudo apt install python3 python3-pip python3-venv
```

**Passo 3: Verificar Instalação**
```bash
python3 --version
```

### 2.4 Linux (Fedora/RedHat)

**Passo 1: Instalar Python**
```bash
sudo dnf install python3 python3-pip
```

**Passo 2: Verificar Instalação**
```bash
python3 --version
```

## 3. Instalação do Git

### 3.1 Windows

**Passo 1: Baixar Git**
1. Acesse: [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Baixe a versão 64-bit
3. Execute o instalador

**Passo 2: Instalar Git**
1. Aceite todas as configurações padrão
2. Clique "Next" em todas as telas
3. Clique "Install"
4. Clique "Finish"

### 3.2 macOS
```bash
brew install git
```

### 3.3 Linux
**Ubuntu/Debian:**
```bash
sudo apt install git
```

**Fedora:**
```bash
sudo dnf install git
```

## 4. Baixando o Compilador Coffee

### 4.1 Clonando o Repositório

**Passo 1: Abrir Terminal/Prompt**
- **Windows**: Pressione `Windows + R`, digite `cmd`
- **macOS/Linux**: Abra o Terminal

**Passo 2: Navegar para uma Pasta**
```bash
# Windows
cd C:\Users\%USERNAME%\Desktop

# macOS/Linux  
cd ~/Desktop
```

**Passo 3: Clonar o Projeto**
```bash
git clone https://github.com/gaekware/coffee.git
cd coffee
```

### 4.2 Verificando os Arquivos

Você deve ver uma estrutura similar a esta:
```
coffee/
├── compilador/
│   └── lexer/
│       ├── parser.py
│       ├── semantic_analyzer.py
│       ├── coffee_interpreter.py
│       └── benchmark_suite.py
├── MANUAL_USUARIO.md
├── MANUAL_INSTALACAO.md
└── README.md
```

## 5. Instalação de Dependências

### 5.1 Criando Ambiente Virtual (Recomendado)

**Por que usar ambiente virtual?**
- Isola as dependências do projeto
- Evita conflitos com outros projetos Python
- Facilita a manutenção

**Passo 1: Criar Ambiente**
```bash
# Windows
python -m venv venv_coffee

# macOS/Linux
python3 -m venv venv_coffee
```

**Passo 2: Ativar Ambiente**
```bash
# Windows
venv_coffee\Scripts\activate

# macOS/Linux
source venv_coffee/bin/activate
```

**Você deve ver `(venv_coffee)` no início da linha do terminal.**

### 5.2 Instalar Bibliotecas

```bash
pip install -r requirements.txt
```

## 6. Testando a Instalação

### 6.1 Teste Básico

**Passo 1: Navegar para a Pasta do Compilador**
```bash
cd compilador/lexer
```

**Passo 2: Executar Teste Simples**
```bash
python coffee_interpreter.py teste_semantico.coffee
```

**Resultado Esperado:**
```
Executando programa Coffee: teste_semantico.coffee
============================================================
1. ANÁLISE SINTÁTICA
------------------------------
AST construída com sucesso!

2. ANÁLISE SEMÂNTICA  
------------------------------
Análise semântica bem-sucedida!

3. EXECUÇÃO DO PROGRAMA
------------------------------
[... saída dos dados ...]

Programa executado com sucesso!
```

### 6.2 Teste Completo

**Executar Suite de Benchmarks:**
```bash
python benchmark_suite.py
```

**Resultado Esperado:**
```
SISTEMA DE BENCHMARKS E TESTES - INTERPRETADOR COFFEE
============================================================
Todos os testes executados com sucesso
Performance: Excelente desempenho verificado
```

## 7. Criando seu Primeiro Programa

### 7.1 Criar Arquivo de Teste

**Passo 1: Criar arquivo `meu_primeiro_programa.coffee`**

**Windows (Notepad):**
1. Clique em "Iniciar" → "Notepad"
2. Digite o código abaixo
3. Salve como `meu_primeiro_programa.coffee` (mude "Tipo" para "Todos os arquivos")

**macOS/Linux:**
```bash
nano meu_primeiro_programa.coffee
```

**Código de exemplo:**
```coffee
dados = load "exemplo.csv"
filtrados = filter dados where valor > 100
resultado = select filtrados (nome, valor)
display resultado
```

### 7.2 Executar seu Programa

```bash
python coffee_interpreter.py meu_primeiro_programa.coffee
```

## 8. Configuração do Editor (Opcional)

### 8.1 Visual Studio Code

**Passo 1: Instalar VS Code**
1. Acesse: [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Baixe e instale para seu sistema

**Passo 2: Abrir Projeto**
1. Abra VS Code
2. File → Open Folder
3. Selecione a pasta `coffee`

**Passo 3: Instalar Extensão Python**
1. Clique no ícone de extensões (quadrado com peça de quebra-cabeça)
2. Procure "Python"
3. Instale a extensão oficial da Microsoft

## 9. Solução de Problemas Comuns

### 9.1 "python não é reconhecido como comando"

**Problema:** Windows não encontra Python
**Solução:**
1. Desinstale Python
2. Reinstale marcando "Add Python to PATH"
3. Ou adicione manualmente ao PATH

### 9.2 "Permission denied"

**Problema:** Erro de permissão no macOS/Linux
**Solução:**
```bash
chmod +x *.py
```

### 9.3 "ModuleNotFoundError: No module named 'pandas'"

**Problema:** Pandas não instalado
**Solução:**
```bash
pip install pandas
```

### 9.4 Ambiente Virtual não Ativa

**Problema:** `(venv_coffee)` não aparece
**Solução:**
```bash
# Desativar se necessário
deactivate

# Reativar
# Windows
venv_coffee\Scripts\activate

# macOS/Linux  
source venv_coffee/bin/activate
```

### 9.5 Git não Encontrado

**Problema:** `git: command not found`
**Solução:**
1. Reinstale o Git
2. Reinicie o terminal
3. Ou baixe o projeto como ZIP do GitHub

## 10. Verificação Final da Instalação

Execute esta lista de verificação:

```bash
# 1. Python funciona?
python --version

# 2. Pandas instalado?
python -c "import pandas; print('OK')"

# 3. Projeto baixado?
ls -la  # (dir no Windows)

# 4. Compilador funciona?
cd compilador/lexer
python coffee_interpreter.py teste_semantico.coffee

# 5. Testes passam?
python benchmark_suite.py
```

**Se todos os comandos funcionaram, sua instalação está completa!**

## 11. Próximos Passos

1. **Leia o Manual do Usuário**: `MANUAL_USUARIO.md`
2. **Experimente os exemplos**: Pasta `compilador/lexer/`
3. **Crie seus próprios programas**: Use os exemplos como base
4. **Explore a documentação**: Leia `DESIGN_BACKEND.md` para detalhes técnicos

## 12. Suporte

Se encontrar problemas:

1. **Verifique os logs de erro** - eles geralmente indicam o problema
2. **Consulte este manual** - a maioria dos problemas está documentada
3. **Execute os testes** - `benchmark_suite.py` ajuda a identificar problemas
4. **Verifique as dependências** - certifique-se de que Python e pandas estão instalados

---

**Parabéns! Você instalou com sucesso o Compilador Coffee!**

Agora você pode começar a escrever programas para análise de dados usando a linguagem Coffee.