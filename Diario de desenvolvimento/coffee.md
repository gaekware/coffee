## Diário de Desenvolvimento

Este documento serve como um registro colaborativo do progresso, decisões e desafios encontrados durante o desenvolvimento da linguagem Coffee.

### Regras de Uso

1.  **Ferramenta:** Este arquivo (`diario_desenvolvimento.md`) será mantido no repositório oficial do projeto no GitHub.
2.  **Frequência:** O diário será atualizado **semanalmente**, preferencialmente após a reunião de alinhamento.
3.  **Responsabilidade:** A atualização do diário é uma **responsabilidade compartilhada** por toda a equipe. Ao final de cada semana, o Gerente de Projeto garantirá que as informações foram registradas.

---

### Registros Semanais

#### **Semana 1: Fundamentos e Planejamento (11/08/2025 - 15/08/2025)**

* **Resumo da Semana:**
    A primeira semana foi focada na estruturação inicial do projeto Coffee. Definimos a visão geral da linguagem, seu público-alvo e objetivos, e o tipo/paradigma. A equipe foi formalizada com a distribuição de papéis e responsabilidades, e os protocolos de colaboração foram estabelecidos. Um cronograma preliminar foi criado para guiar as próximas etapas.

* **Decisões Tomadas:**
    * **Nome da Linguagem:** Coffee, com a analogia de "grãos" (dados) e "filtro" (compilador Strainer).
    * **Público-Alvo:** Iniciantes em ciência de dados, com foco em simplificar a manipulação de dados.
    * **Ferramentas:** Jira para gestão de tarefas e GitHub para controle de versão.
    * **Reuniões:** Uma reunião síncrona semanal.
    * **Estrutura do Diário:** Definido o template e a frequência de atualização.

* **Desafios Encontrados:**
    * Nenhum desafio significativo nesta fase inicial, focada em planejamento.

* **Observações Adicionais:**
    * A equipe demonstrou bom engajamento e alinhamento durante as discussões iniciais.
    * A proposta da linguagem foi bem recebida e gerou entusiasmo.

#### **Semana 2: Decisões de Design Léxico (18/08/2025 - 22/08/2025)**

* **Decisão sobre o Alfabeto:**
    * Optamos por um subconjunto do ASCII para o alfabeto inicial da Coffee. A justificativa é manter a linguagem simples e acessível, evitando as complexidades do Unicode nesta fase inicial. Isso garante que qualquer teclado padrão possa ser usado e que o processamento de caracteres seja direto.

* **Definição de Identificadores:**
    * Adotamos o padrão (letra | _)(letra | digito | _)*, comum em linguagens como Python e C. Decidimos que os identificadores serão case-sensitive (ex: Vendas é diferente de vendas). Essa escolha, embora exija mais atenção do programador, é o padrão na maioria das linguagens modernas e ensina uma boa prática de consistência.

* **Estilo dos Comentários:** 
    * Escolhemos o # para comentários de linha única. Essa decisão foi fortemente influenciada pelo nosso público-alvo, que provavelmente tem familiaridade com Python, uma linguagem onipresente em ciência de dados. Isso reduz a carga cognitiva e torna o código mais intuitivo para eles.

* **Literais Numéricos e de String:** 
    * Definimos string com aspas duplas e números inteiros e de ponto flutuante. Não incluímos notação científica ou outros formatos numéricos complexos por enquanto, para manter o foco na simplicidade. A prioridade é cobrir os casos de uso mais comuns em análise de dados básica.

* **Ambiguidade:** 
    * Tivemos cuidado para que as definições não gerassem ambiguidades. Por exemplo, um identificador não pode começar com um dígito para não ser confundido com um número. Da mesma forma, as palavras-chave são reservadas e não podem ser usadas como identificadores.