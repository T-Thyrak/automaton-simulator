from __future__ import annotations
#! ^^^^^ this is a future import, it moves the annotations evaluation to *after* the class definition

import json

from telegram import Update
from telegram.ext import CallbackContext

from state import State
from sym import Symbol

from context import Context


class FA:
    def __init__(self, states: list[State] = None, alphabet: list[Symbol] = None, transitions: dict[tuple[State, Symbol], list[State]] = None, start_state: State = None, final_states: list[State] = None):
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

    def add_states_str(self, states: list[str]) -> bool:
        """Add states from a list of strings."""
        return self.add_states(states_list_from_str(states))

    def add_states(self, states: list[State]) -> bool:
        """Add states to the FA."""

        has_added = False
        for state in states:
            print(f"Adding state {state}")
            # no duplicates
            if state not in self.states:
                self.states.append(state)
                has_added = True

        if has_added:
            # sort ascending
            self.states.sort(key=lambda state: state.id)

        return has_added
    
    def add_start_state_str(self, start_state: str) -> bool:
        """Add states from a list of strings."""
        return self.add_start_state(State(int(start_state[1:])))

    def add_start_state(self, start_state: State) -> bool:
        """Add states to the FA."""
        print(f"Adding state {start_state}") 
        self.start_state=start_state
        return True
            

    ## Add Final State
    def add_final_states_str(self, final_states: list[str]) -> bool:
        """Add states from a list of strings."""
        return self.add_final_states(final_states_list_from_str(final_states))

    def add_final_states(self, final_states: list[State]) -> bool:
        """Add states to the FA."""

        has_added = False
        for final_states in final_states:
            print(f"Adding final state {final_states}")
            print (final_states)

            # no duplicates
            if final_states not in self.final_states:
                self.final_states.append(final_states)
                has_added = True

        if has_added:
            # sort ascending
            self.final_states.sort(key=lambda final_states: final_states                              .id)

        return has_added
    
    
    def delete_states_str(self, states: list[str]) -> bool:
        """Delete states from a list of strings."""
        return self.delete_states(states_list_from_str(states))

    def delete_states(self, states: list[State]) -> bool:
        """Delete states from the FA."""
        has_deleted = False
        for state in states:
            if state in self.states:
                self.states.remove(state)
                has_deleted = True

        if has_deleted:
            # sort ascending
            self.states.sort(key=lambda state: state.id)

        return has_deleted

    def json_serialize(self, indent: int = 4) -> str:
        """Serialize the FA to JSON."""

        d = {
            "states": [str(state) for state in self.states],
            "alphabet": [str(symbol) for symbol in self.alphabet],
            "starting_state": str(self.start_state),
            "final_states": [str(state) for state in self.final_states],
            "transition_function": sorted(list(map(lambda transition: {
                "from_state": str(transition[0][0]),
                "with_symbol": str(transition[0][1]),
                "to_state": [str(state) for state in transition[1]]
            }, self.transitions.items())), key=lambda transition: (transition['from_state'], transition['with_symbol']))
        }

        return json.dumps(d, indent=indent)

    def json_deserialize(json_str: str) -> 'FA' | None:
        """Deserialize the FA from JSON."""
        
        try:
            json.loads(json_str)
        except json.decoder.JSONDecodeError:
            return None
        
        d = json.loads(json_str)
        
        fa = FA.default()
        fa.states = states_list_from_str(list(map(lambda s: s[1:], d['states'])))
        fa.alphabet = symbols_list_from_str(d['alphabet'])
        fa.starting_state = State(int(d['starting_state'][1:]))
        fa.final_states = states_list_from_str(list(map(lambda s: s[1:], d['final_states'])))
        
        fa.transitions = {}
        
        for transition in d['transition_function']:
            from_state = State(int(transition['from_state'][1:]))
            with_symbol = Symbol(transition['with_symbol'])
            to_state = states_list_from_str(list(map(lambda s: s[1:], transition['to_state'])))
            
            fa.transitions[(from_state, with_symbol)] = to_state
        
        return fa
                
    def __repr__(self):
        return f"FA(states={self.states}, alphabet={self.alphabet}, transitions={self.transitions}, start_state={self.start_state}, final_states={self.final_states})"


def states_list_from_str(states: list[str]) -> list[State]:
    return [State(int(state[1:])) for state in states]

def start_state_list_from_str(start_state: str) -> State:
    return (start_state)
def final_states_list_from_str(final_states: list[str]) -> list[State]:
    return [State(int(final_states[1:])) for final_states in final_states]

def symbols_list_from_str(symbols: list[str]) -> list[Symbol]:
    return [Symbol(symbol) for symbol in symbols]


def fa_debug(update: Update, context: CallbackContext) -> None:
    """Prints the FA in debug mode."""

    if Context.context.get(update.effective_user.id) is None:
        Context.context[update.effective_user.id] = {
            "fa": FA.default(),
            "id": None,
            "mode": None,
            "tmp": {}
        }
        update.message.reply_text(
            "You have not created an FA yet, so I made one for you.")

    fa = Context.context[update.effective_user.id]['fa']

    update.message.reply_text(f"Debug information:\n\n{fa.json_serialize()}")


def test_debug(update: Update, context: CallbackContext) -> None:
    fa = FA(
        states=[
            State(0),
            State(2),
            State(3),
        ],
        alphabet=[
            Symbol('a'),
            Symbol('b'),
        ],
        start_state=State(0),
        final_states=[
            State(3),
        ],
        transitions={
            (State(2), Symbol('b')): [State(3)],
            (State(0), Symbol('a')): [State(2), State(0)],
        }
    )

    update.message.reply_text(f"Debug information:\n\n{fa.json_serialize()}")
