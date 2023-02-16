from state import State
from sym import Symbol

class FA:
    def __init__(self, states: list[State] = None, alphabet: list[Symbol] = None, transitions: dict[tuple[State, Symbol], State] = None, start_state: State = None, final_states: list[State] = None):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
        
    def default():
        return FA(
            states=[],
            alphabet=[],
            transitions={},
            start_state=None,
            final_states=[],
        )