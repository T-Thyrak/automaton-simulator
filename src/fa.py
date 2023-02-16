from state import State
from sym import Symbol

class FA:
    def __init__(self, states: list[State], alphabet: list[Symbol], transitions: dict[tuple[State, Symbol], State], start_state: State, final_states: list[State]):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states