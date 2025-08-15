# Entrega da Semana 1: Fundamentos e Planejamento - Projeto Coffee

Este documento centraliza todas as entregas da primeira semana de desenvolvimento da linguagem de programação Coffee, incluindo a proposta inicial, a definição da equipe, o cronograma preliminar e o modelo do diário de desenvolvimento.

---

## Proposta Inicial da Linguagem: Coffee

### 1. Visão Geral

**Coffee** é uma linguagem de programação projetada para transformar e refinar dados brutos de maneira intuitiva e acessível. A filosofia da linguagem é baseada na analogia de que dados são como "grãos" de café (`Coffee`), que precisam ser processados por um "filtro" (`Strainer`), nosso compilador, para se tornarem insights valiosos.

Nosso lema é: **"A linguagem que transforma e refina."**

### 2. Público-Alvo e Objetivos

A linguagem **Coffee** é destinada a **iniciantes na área de ciência de dados**. Nosso público-alvo são estudantes e entusiastas que possuem um conhecimento básico de programação, similar ao nível iniciante em Python, e que não precisam se preocupar com a complexidade da tipagem de dados em seus primeiros projetos.

O principal problema que buscamos resolver é a alta curva de aprendizado das ferramentas de análise de dados existentes. **Coffee** visa simplificar esse processo, oferecendo uma sintaxe mais abstrata e comandos de alto nível, permitindo que o usuário se concentre na lógica da manipulação dos dados, e não em complexidades sintáticas.

### 3. Tipo e Paradigma

**Coffee** está sendo concebida como uma linguagem de **uso geral** com um forte viés para o **ensino de programação** no domínio de dados.

Nesta fase inicial, não estamos nos prendendo a um único paradigma de programação (como orientado a objetos ou funcional). A estrutura da linguagem será desenvolvida de forma pragmática para melhor atender às necessidades de simplicidade e clareza para o nosso público-alvo.

---

## Definição de Equipe, Papéis e Protocolos

### 1. Membros da Equipe

- Gustavo
- Adrian
- Eduardo
- Kauê

### 2. Papéis e Responsabilidades

Para garantir uma organização eficiente, os papéis foram distribuídos da seguinte forma, alinhando as responsabilidades com as diferentes frentes do projeto.

| Papel | Responsável Principal | Responsabilidades | Interesses Mapeados |
| :--- | :--- | :--- | :--- |
| **Gerente de Projeto** | Adrian | - Organizar o backlog de tarefas no Jira.<br>- Garantir a comunicação e o alinhamento da equipe.<br>- Liderar as reuniões semanais.<br>- Responsável pela entrega final das atividades. | Visão geral do projeto e organização. |
| **Arquiteto da Linguagem** | Gustavo | - Liderar o design da sintaxe e semântica da linguagem.<br>- Definir a gramática formal.<br>- Pesquisar as bases teóricas para as funcionalidades. | Foco na parte teórica (gramática, semântica). |
| **Desenvolvedor Principal** | Kauê | - Liderar a implementação do compilador/interpretador (`Strainer`).<br>- Codificar o analisador léxico e sintático (parser).<br>- Transformar a teoria em código funcional. | Foco na implementação (parser, interpretador). |
| **Gerente de Qualidade e Documentação** | Eduardo | - Criar e manter a documentação oficial da linguagem.<br>- Desenvolver exemplos de código e tutoriais.<br>- Liderar a criação de testes para validar o compilador. | Foco em documentar, criar exemplos e testes. |

*Observação: Todos os membros da equipe são incentivados a colaborar em todas as frentes para maximizar o aprendizado e o compartilhamento de conhecimento.*

### 3. Protocolos de Colaboração

- **Ferramenta de Gestão:** Todas as tarefas serão gerenciadas através do **Jira**.
- **Repositório de Código:** O código e toda a documentação do projeto serão armazenados em um repositório no **GitHub**.
- **Frequência de Reuniões:** Teremos **uma reunião síncrona por semana** para alinhamento, discussão de impedimentos e planejamento dos próximos passos.
- **Responsável pela Entrega:** O **Gerente de Projeto (Adrian)** centralizará os arquivos e realizará a submissão da tarefa no sistema.

---

## Cronograma Preliminar do Projeto

Este cronograma serve como um guia inicial para as próximas semanas. As metas e datas podem ser ajustadas conforme o andamento do projeto.

| Semana | Objetivo Principal | Tarefas Sugeridas |
| :--- | :--- | :--- |
| **Semana 1** | Fundamentos e Planejamento | - Definição da Proposta Inicial.<br>- Divisão de papéis e responsabilidades.<br>- Configuração das ferramentas (GitHub, Jira). |
| **Semana 2** | Definição da Gramática | - Pesquisar sobre notações de gramática (ex: EBNF).<br>- Escrever a primeira versão da gramática da Coffee.<br>- Definir o conjunto de palavras-chave e operadores. |
| **Semana 3** | Análise Léxica | - Estudar ferramentas e conceitos de analisadores léxicos.<br>- Implementar o "scanner" que transforma o código-fonte em uma sequência de tokens. |
| **Semana 4** | Análise Sintática (Parsing) | - Estudar algoritmos de parsing (ex: LL, LR).<br>- Implementar o "parser" que valida a estrutura do código com base na gramática e gera uma Árvore Sintática Abstrata (AST). |
| **Semana 5** | Análise Semântica | - Iniciar a implementação das checagens de regras semânticas (ex: uso de variáveis não declaradas, etc.).<br>- Refinar a estrutura da AST. |

---

## Diário de Desenvolvimento

Este documento marca o ponto de partida do nosso projeto. Para acompanhar o progresso contínuo, as decisões e os desafios semanais, consulte o **Diário de Desenvolvimento**. Ele será atualizado regularmente e servirá como um registro detalhado da evolução da linguagem Coffee.

[Acessar Diário de Desenvolvimento](/Diario%20de%20desenvolvimento/coffee.md)