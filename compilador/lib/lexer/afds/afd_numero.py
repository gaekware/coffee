
from ..token import Token, TokenType
from ..afd_base import AfdBase

class AfdNumero(AfdBase):
    def process(self, source: str, start_index: int) -> Token | None:
        
        
        transitions = {
            0: {'digit': 1},
            1: {'digit': 1, 'dot': 2},
            2: {'digit': 3},
            3: {'digit': 3}
        }
        
        final_states = {1, 3}

        current_state = 0
        current_index = start_index
        
        
        last_final_state_index = -1

        while current_index < len(source):
            char = source[current_index]
            char_type = self._get_char_type(char)

            if char_type in transitions.get(current_state, {}):
                current_state = transitions[current_state][char_type]
                current_index += 1
                if current_state in final_states:
                    last_final_state_index = current_index
            else:
                break  

        if last_final_state_index != -1:
            lexeme = source[start_index:last_final_state_index]
            return Token(TokenType.NUMBER, lexeme, start_index)
        
        return None

    def _get_char_type(self, char: str) -> str:
        if char.isdigit():
            return 'digit'
        if char == '.':
            return 'dot'
        return 'other'