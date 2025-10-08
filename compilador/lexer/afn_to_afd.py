class NFA:
    """
    Estrutura para representar um Autômato Finito Não-Determinístico (AFN).
    """
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  # Dicionário: (state, symbol) -> set of states
        self.start_state = start_state
        self.final_states = final_states

def epsilon_closure(nfa: NFA, states: set):
    """
    Calcula o fecho-épsilon de um conjunto de estados no AFN.
    """
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        # Transições em épsilon (representado por '')
        next_states = nfa.transitions.get((state, ''), set())
        for next_state in next_states:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return frozenset(closure)

def move(nfa: NFA, states: set, symbol: str):
    """
    Calcula o conjunto de estados alcançáveis a partir de um conjunto de estados
    com um determinado símbolo.
    """
    result = set()
    for state in states:
        next_states = nfa.transitions.get((state, symbol), set())
        result.update(next_states)
    return frozenset(result)

def convert_nfa_to_dfa(nfa: NFA):
    """
    Implementação do algoritmo de construção de subconjuntos para converter um AFN em AFD.
    """
    dfa_states = set()
    dfa_transitions = {}
    dfa_start_state = epsilon_closure(nfa, {nfa.start_state})
    dfa_final_states = set()

    unmarked_states = [dfa_start_state]
    dfa_states.add(dfa_start_state)
    
    # Mapeia os estados do AFD (frozensets) para nomes mais simples (ex: S0, S1)
    state_map = {dfa_start_state: "S0"}
    next_state_id = 1

    while unmarked_states:
        current_dfa_state_set = unmarked_states.pop(0)
        
        # Se qualquer estado do AFN no conjunto atual for final, o estado do AFD é final.
        if any(s in nfa.final_states for s in current_dfa_state_set):
            dfa_final_states.add(state_map[current_dfa_state_set])

        for symbol in nfa.alphabet:
            # Calcula o próximo estado do AFD
            next_nfa_states = move(nfa, current_dfa_state_set, symbol)
            next_dfa_state_set = epsilon_closure(nfa, next_nfa_states)

            if not next_dfa_state_set:
                continue

            if next_dfa_state_set not in dfa_states:
                dfa_states.add(next_dfa_state_set)
                unmarked_states.append(next_dfa_state_set)
                # Adiciona um novo nome para o novo estado do AFD
                state_map[next_dfa_state_set] = f"S{next_state_id}"
                next_state_id += 1
            
            # Adiciona a transição ao AFD
            current_state_name = state_map[current_dfa_state_set]
            next_state_name = state_map[next_dfa_state_set]
            dfa_transitions[(current_state_name, symbol)] = next_state_name

    # Retorna uma representação simplificada do AFD
    return {
        "states": set(state_map.values()),
        "alphabet": nfa.alphabet,
        "transitions": dfa_transitions,
        "start_state": state_map[dfa_start_state],
        "final_states": dfa_final_states
    }