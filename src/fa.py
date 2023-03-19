from __future__ import annotations
#! ^^^^^ this is a future import, it moves the annotations evaluation to *after* the class definition

import json
import copy

from telegram import Update
from telegram.ext import CallbackContext

from state import State
from sym import Symbol

from ext.anything import union, difference
from ext.result import Result

from context import Context
from ext.anything import table_drop, position_of, choose, prune_none

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
            self.states.sort(key=lambda state: state.symbol)

        return has_added
   
     #add symbol str
    def add_symbols_str(self, symbol: list[str]) -> bool:
        """Add symbols from a list of strings."""

        return self.add_symbols(symbols_list_from_str(symbol))

    def add_symbols(self, symbols: list[Symbol]) -> bool:
        """Add symbols to the FA."""

        has_added = False
        for symbol in symbols:
            print(f"Adding symbol {symbol}")
            # no duplicates
            if symbol not in self.alphabet:
                self.alphabet.append(symbol)
                has_added = True

        if has_added:
            # sort ascending
            self.alphabet.sort(key=lambda symbol: symbol.symbol)
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
        return self.add_final_states(states_list_from_str(final_states))

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
            self.final_states.sort(key=lambda final_states: final_states.id)

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
            self.states.sort(key=lambda state: state.symbol)

        return has_deleted
    
    # delete symbol
    def delete_symbol_str(self, symbol: list[Symbol]) -> bool:
        """Delete states from a list of strings."""
        return self.delete_symbols(symbols_list_from_str(symbol))

    def delete_symbols(self, symbols: list[Symbol]) -> bool:
        """Delete states from the FA."""
        has_deleted = False
        for symbol in symbols:
            print(f"Deleting symbol {symbol}")

            if symbol in self.alphabet:
                self.alphabet.remove(symbol)
                has_deleted = True

        if has_deleted:
            # sort ascending
            self.alphabet.sort(key=lambda symbol: symbol.symbol)

        return has_deleted
    
     # delete start state 
    def delete_start_state_str(self, start_state: str) -> bool:
        """Add states from a list of strings."""
        return self.delete_start_state(State(int(start_state[1:])))

    def delete_start_state(self, start_state: State) -> bool:
        """Delete Start State to the FA."""
        print(f"Deteting Start_State {start_state}") 

        self.start_state=''
        return True
   
    # delete final_state

    def delete_final_states_str(self, final_states: list[str]) -> bool:
        """Add states from a list of strings."""
        return self.delete_final_states(final_states_list_from_str(final_states))

    def delete_final_states(self, final_states: list[State]) -> bool:
        """Deleting Final State to the FA."""

        has_deleted = False
        for final_states in final_states:
            print(f"Deleting final state {final_states}")

            # no duplicates
            if final_states in self.final_states:
                self.final_states.remove(final_states)
                has_deleted = True

        if has_deleted:
            # sort ascending
            self.final_states.sort(key=lambda final_states: final_states.id)

        return has_deleted
    # delete transition
    
    def add_transition_str(self, from_state: str, with_symbol: str, to_states: list[str]) -> Result[bool, str]:
        """Add a transition from a string."""
        from_state_obj = State(int(from_state[1:]))

        if with_symbol == "eps":
            with_symbol_obj = Symbol.epsilon_symbol()
        else:
            with_symbol_obj = Symbol(with_symbol)
        
        to_states_list = states_list_from_str(to_states)
        
        return self.add_transition(from_state_obj, with_symbol_obj, to_states_list)
    
    def add_transition(self, from_state: State, with_symbol: Symbol, to_states: list[State]) -> Result[bool, str]:
        """Add a transition to the FA."""
        has_added = False
        
        if from_state not in self.states:
            return Result.Err(f"State {from_state} does not exist.")
        
        if with_symbol not in self.alphabet and with_symbol != Symbol.epsilon_symbol():
            return Result.Err(f"Symbol {with_symbol} does not exist.")
        
        for state in to_states:
            if state not in self.states:
                return Result.Err(f"State {state} does not exist.")
        
        if self.transitions.get((from_state, with_symbol)) is not None:
            # do merge
            last_transition = self.transitions[(from_state, with_symbol)]
            self.transitions[(from_state, with_symbol)] = union(last_transition, to_states, key=lambda s1, s2: s1.id == s2.id)
            has_added = True
        else:
            self.transitions[(from_state, with_symbol)] = to_states
            has_added = True
        
        return Result.Ok(has_added)
    
    def delete_transition_str(self, from_state: str, with_symbol: str, to_states: list[str]) -> Result[bool, str]:
        """Delete a transition from a string."""
        from_state_obj = State(int(from_state[1:]))
        with_symbol_obj = Symbol(with_symbol)
        
        to_states_list = states_list_from_str(to_states)
        
        return self.delete_transition(from_state_obj, with_symbol_obj, to_states_list)
    
    def delete_transition(self, from_state: State, with_symbol: Symbol, to_states: list[State]) -> Result[bool, str]:
        """Delete a transition from the FA."""
        has_deleted = False
        
        if from_state not in self.states:
            return Result.Err(f"State {from_state} does not exist.")
        
        if with_symbol not in self.alphabet:
            return Result.Err(f"Symbol {with_symbol} does not exist.")
        
        if self.transitions.get((from_state, with_symbol)) is not None:
            # do merge
            last_transition = self.transitions[(from_state, with_symbol)]
            self.transitions[(from_state, with_symbol)] = difference(last_transition, to_states, key=lambda s1, s2: s1.id == s2.id)
            has_deleted = True
            
            if len(self.transitions[(from_state, with_symbol)]) == 0:
                del self.transitions[(from_state, with_symbol)]
        
        return Result.Ok(has_deleted)
    
    def delete_transition_index_str(self, index: str, states: list[str] | None) -> Result[bool, str]:
        """Delete a transition from a string."""
        index_obj = int(index)
        
        if states is None:
            states_list = []
        else:
            states_list = states_list_from_str(states)
        
        return self.delete_transition_index(index_obj, states_list)
    
    def delete_transition_index(self, index: int, states: list[State]) -> Result[bool, str]:
        """Delete a transition from the FA."""
        has_deleted = False
        
        if index < 0 or index >= len(self.transitions):
            return Result.Err(f"Index {index} is out of bounds.")
        
        transition = sorted(self.transitions.items(), key=lambda t: (t[0][0].id, t[0][1].symbol))[index]
        from_state = transition[0][0]
        with_symbol = transition[0][1]
        # to_states = transition[1]
        
        if self.transitions.get((from_state, with_symbol)) is not None:
            # do merge
            last_transition = self.transitions[(from_state, with_symbol)]
            diff = difference(last_transition, states, key=lambda s1, s2: s1.id == s2.id)
            self.transitions[(from_state, with_symbol)] = diff
            has_deleted = True
            
            if len(self.transitions[(from_state, with_symbol)]) == 0:
                del self.transitions[(from_state, with_symbol)]
        
        return Result.Ok(has_deleted)
    
    # *** UTILITIES ***

    def json_serialize(self, indent: int | None = 4) -> str:
        """Serialize the FA to JSON.
        
        Args:
            indent (int, optional): Indentation. Defaults to 4. (None for no indentation)"""

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
        except json.decoder.JSONDecodeError as e:
            print(f"JSONPARSINGERROR:\n{e.msg = }\n{e.doc = }\n{e.pos = }\n{e.lineno = }\n{e.colno = }")
            return None
        
        d = json.loads(json_str)
        
        fa = FA.default()
        fa.states = states_list_from_str(d['states'])
        fa.alphabet = symbols_list_from_str(d['alphabet'])
        fa.start_state = State(int(d['starting_state'][1:]))
        fa.final_states = states_list_from_str(d['final_states'])
        
        fa.transitions = {}
        
        for transition in d['transition_function']:
            from_state = State(int(transition['from_state'][1:]))
            with_symbol = Symbol(transition['with_symbol'])
            to_state = states_list_from_str(transition['to_state'])
            
            fa.transitions[(from_state, with_symbol)] = to_state
        
        return fa
    
    def pretty_transition(self, with_counter: bool = False) -> str:
        sorted_transitions = sorted(self.transitions.items(), key=lambda transition: (transition[0][0].id, transition[0][1].symbol))
        
        if len(sorted_transitions) == 0:
            return "[]"

        counter = 1
        
        sb = "[\n"
        for transition in sorted_transitions:
            if not with_counter:
                sb += f"    {str(transition[0][0])} --- {str(transition[0][1])} --> {str(list(map(str, transition[1])))}\n"
            else:
                sb += f"    {counter}. {str(transition[0][0])} --- {str(transition[0][1])} --> {str(list(map(str, transition[1])))}\n"
                counter += 1
        sb += "]"
        
        return sb
    
    def _copy(self) -> FA:
        """Performs deep copy of the FA."""
        states = copy.deepcopy(self.states)
        alphabet = copy.deepcopy(self.alphabet)
        transitions = copy.deepcopy(self.transitions)
        start_state = copy.deepcopy(self.start_state)
        final_states = copy.deepcopy(self.final_states)
        
        return FA(states, alphabet, transitions, start_state, final_states)
    
    def test_accept_str(self, input_str: str) -> Result[bool, str]:
        """Test whether a string is accepted by the FA.

        Args:
            input_str (str): The string to test

        Returns:
            Result[bool, str]: The result of the test. Ok(true) if accepted, Ok(false) if rejected. Err if undecidable.
        """
        
        verify_result = self.verify_fa()
        if verify_result.is_err():
            return verify_result
        
        if verify_result.unwrap():
            return self._test_accept_str_nfa(input_str)
        else:
            return self._test_accept_str_dfa(input_str)
        
    def _test_accept_str_dfa(self, input_str: str) -> Result[bool, str]:
        """Test whether a string is accepted by the DFA.

        Args:
            input_str (str): The string to test

        Returns:
            Result[bool, str]: The result of the test. Ok(true) if accepted, Ok(false) if rejected. Err if undecidable.
        """
        
        if len(self.transitions) == 0:
            return Result.Err("There is no transitions to check.")
        
        current_state = self.start_state
        for c in input_str:
            symbol = Symbol(c)
            if symbol not in self.alphabet:
                return Result.Err(f"Symbol {symbol} is not in the alphabet.")
            
            if self.transitions.get((current_state, symbol)) is None:
                return Result.Ok(False)
            
            current_state = self.transitions[(current_state, symbol)][0]
        
        return Result.Ok(current_state in self.final_states)
    
    def _test_accept_str_nfa(self, input_str: str) -> Result[bool, str]:
        """Test whether a string is accepted by the NFA.

        Args:
            input_str (str): The string to test

        Returns:
            Result[bool, str]: The result of the test. Ok(true) if accepted, Ok(false) if rejected. Err if undecidable.
        """
        if len(self.transitions) == 0:
            return Result.Err("There is no transitions to check.")
        
        return self._try_accept_state(self.start_state, input_str)
        
    def _try_accept_state(self, starting_state: State, input_str: str) -> Result[bool, str]:
        """Try to accept the state. If there is still input string, call this function recursively.

        Args:
            state (State): Current state
            input_str (str): Input string

        Returns:
            Result[bool, str]: The result of the test. Ok(true) if accepted, Ok(false) if rejected. Err if undecidable.
        """
        if len(input_str) == 0:
            return Result.Ok(starting_state in self.final_states)
        
        symbol = Symbol(input_str[0])
        next_states = self.transitions.get((starting_state, symbol))
        
        if next_states is not None:
            for next_state in next_states:
                result = self._try_accept_state(next_state, input_str[1:])
                if result.is_ok() and result.unwrap():
                    return result
        
        epsilon_states = self.transitions.get((starting_state, Symbol.epsilon_symbol()))
        if epsilon_states is not None:
            for epsilon_state in epsilon_states:
                result = self._try_accept_state(epsilon_state, input_str)
                if result.is_ok() and result.unwrap():
                    return result
                
        return Result.Ok(False)
    
    def verify_fa(self) -> Result[bool, str]:
        """Verify whether FA is a NFA or DFA.
        
        Args:
            fa (FA): The FA to test
        
        Returns:
            Result[bool, str]: The result of the verification. Ok(true) if NFA, Ok(false) if DFA. Err if undecidable.
        """
        
        if len(self.transitions) == 0:
            return Result.Err("There is no transitions to check.")
        
        for t in self.transitions.items():
            # check if symbol contain epsilon
            if t[0][1] == Symbol.epsilon_symbol():
                return Result.Ok(True)
            # check if to_state have many states
            if len(t[1]) > 1:
                return Result.Ok(True)

        return Result.Ok(False)
    
    def _epsilon_closure(self, states: set[State]) -> set[State]:
        """Calculate the epsilon closure of a set of states.

        Args:
            states (set[State]): The set of states to calculate the epsilon closure of.

        Returns:
            set[State]: The epsilon closure of the set of states.
        """
        out_closure = set(states)
        
        for state in states:
            if self.transitions.get((state, Symbol.epsilon_symbol())) is not None:
                out_closure = out_closure.union(self.transitions[(state, Symbol.epsilon_symbol())])

        return out_closure
    
    def determinize(self) -> Result[FA, str]:
        """Determinize an *NFA* with the Subset Construction Algorithm.

        Returns:
            Result[FA, str]: The result of the determinization. Ok if successful, Err if not. Will Err if the FA is not an NFA.
        """
        
        verify_result = self.verify_fa()
        if verify_result.is_err():
            return Result.Err(verify_result.unwrap_err())
        
        if verify_result.unwrap() == False:
            return Result.Err("Cannot determinize a DFA.")

        dfa_states = [State(0)]
        dfa_starting_state = State(0)
        
        # a frozenset is a set that is immutable
        # easy, right?
        mapping: dict[frozenset, State] = {
            frozenset(self._epsilon_closure({self.start_state})): State(0)
        }
        
        dfa_transition_table: dict[tuple[State, Symbol], list[State]] = {}
        
        # we're indexing the states as we encounter them
        counter = 0
        
        # message processing style queue
        queue = [self._epsilon_closure({self.start_state})]
        
        while len(queue) > 0:
            # FIFO, so we pop the first element
            current_multi_state = queue.pop(0)
            
            # for each symbol in the alphabet
            for symbol in self.alphabet:
                # create a union of all the states that can be reached from the current state with the symbol
                next_multi_state = set()
                for state in current_multi_state:
                    if self.transitions.get((state, symbol)) is not None:
                        next_multi_state = next_multi_state.union(self.transitions[(state, symbol)])
                
                next_multi_state = self._epsilon_closure(next_multi_state)
                
                # find the state corresponding to the current multi-state
                current_state = mapping[frozenset(current_multi_state)]
                
                if len(next_multi_state) > 0:
                    # if the next multi-state is not in the mapping, add it
                    if frozenset(next_multi_state) not in mapping:
                        counter += 1
                        dfa_states.append(State(counter))
                        mapping[frozenset(next_multi_state)] = State(counter)
                        queue.append(next_multi_state)
                        
                    # find the id of the next multi-state
                    next_state = mapping[frozenset(next_multi_state)]
                    
                    # add the transition to the transition table
                    dfa_transition_table[(current_state, symbol)] = [next_state]
        
        # construct the set of final states
        dfa_final_states = []
        for multi_state in mapping:
            for state in multi_state:
                if state in self.final_states:
                    dfa_final_states.append(mapping[multi_state])
                    break
            
        return Result.Ok(
            FA(
                states=dfa_states,
                alphabet=copy.deepcopy(self.alphabet),
                transitions=dfa_transition_table,
                start_state=dfa_starting_state,
                final_states=dfa_final_states
            )    
        )
    
    def minimize(self) -> Result[FA, str]:
        """Minimize a *DFA* with the Table-Filling Algorithm."""
        
        result = self.verify_fa()
        if result.is_err():
            return Result.Err(result.unwrap_err())
        
        if result.unwrap() == True:
            return Result.Err("Cannot minimize a NFA.")
        
        # * Step 1. Remove unreachable states
        reachable_states = set()
        reachable_states.add(self.start_state)
        for state in self.states:
            for symbol in self.alphabet:
                # if there is a transition from state with any symbol, it is reachable
                if self.transitions.get((state, symbol)) is not None:
                    reachable_states.add(self.transitions[(state, symbol)][0])
                    
        # Convert to sorted list, for consistency
        reachable_states = sorted(list(reachable_states), key=lambda state: state.id)
        
        # * Step 2. Mark final and non-final states pair
        mark_table: dict[tuple[int, int], bool] = {}
        for state1 in reachable_states:
            for state2 in reachable_states:
                is_final1 = state1 in self.final_states
                is_final2 = state2 in self.final_states

                if (is_final1 and not is_final2) or (is_final2 and not is_final1):
                    mark_table[(state1.id, state2.id)] = True
                else:
                    mark_table[(state1.id, state2.id)] = False
                    
        # * Step 3. Mark pairs of states
        while True:
            #! ^i hate non-locals more than while True
            
            old_mark_table = copy.deepcopy(mark_table)
            
            for state1 in reachable_states:
                for state2 in reachable_states:
                    for symbol in self.alphabet:
                        # nice day to have O(n^4) algorithm
                        
                        out_states1 = self.transitions.get((state1, symbol))
                        out_states2 = self.transitions.get((state2, symbol))
                        
                        # if the output states of both the states are marked, then mark the pair of original states
                        if out_states1 is not None and out_states2 is not None:
                            mark = mark_table.get((out_states1[0].id, out_states2[0].id))
                            if mark is not None and mark == True:
                                mark_table[(state1.id, state2.id)] = True
            
            if old_mark_table == mark_table:
                break
        
        # drop half of the table, as it is symmetric
        mark_table = table_drop(mark_table, key=lambda x, y: x >= y)
        
        # * Step 4. Create equivalence classes
        equivalence_classes: list[set[State]] = []
        available_states: list[State] = copy.deepcopy(reachable_states)
        
        while len(available_states) != 0:
            state = available_states[0]
            equivalence_class = set([state])
            
            for state2 in available_states:
                min_key = min(state.id, state2.id)
                max_key = max(state.id, state2.id)
                
                mark = mark_table.get((min_key, max_key))
                if mark is not None and not mark:
                    equivalence_class.add(state2)

            equivalence_classes.append(equivalence_class)
            available_states = list(filter(lambda x: x not in equivalence_class, available_states))
            
        # * Step 5. Create new states
        # the new states are the equivalence classes
        new_states: list[State] = list(map(lambda x: State(x), range(len(equivalence_classes))))
        
        # the initial state is the equivalence class of the initial state
        # ? I do wonder why that is unique.
        
        new_initial_state: State = position_of(equivalence_classes, key=lambda x: self.start_state in x)
        if new_initial_state is None:
            return Result.Err("Absurd error: Initial state not found in equivalence classes.")
        
        # the final states are the equivalence classes that contain a final state
        # !and yes, I am a big fan of functional programming
        # !but Python makes everything a function instead of composing them
        
        # Explanation: This thing loops over each equivalence classes
        # then loops over each state in the equivalence class to check if it is a final state, and retains the ones that are
        # then we check that if there is even at least one left over per equivalence class
        # then the equivalence class is a final state, and retained.
        
        new_final_states_classes: list[set[State]] = list(filter(lambda x: len(list(filter(lambda y: y in self.final_states, x))) > 0, equivalence_classes))
        new_final_states = list(map(lambda x: State(position_of(equivalence_classes, key=lambda y: x == y)), new_final_states_classes))
        new_transitions: dict[tuple[State, Symbol], list[State]] = {}
        
        # our method of setting the transition is indexing as we go
        # very buggy, but it works in Rust, so it should work here too
        for i, equivalence_class in enumerate(equivalence_classes):
            for symbol in self.alphabet:
                # pick a random state in the equivalence class
                state = choose(equivalence_class)
                
                # find delta[state, symbol]
                out_states = self.transitions.get((state, symbol))
                
                # set the new transition if None
                if out_states is None:
                    new_transitions[(State(i), symbol)] = None
                    continue
                    
                out_state = out_states[0]
                
                # find the equivalence class index of the output state
                out_equivalence_class_index = position_of(equivalence_classes, key=lambda x: out_state in x)
                
                # actually set the new transition
                new_transitions[(State(i), symbol)] = [State(out_equivalence_class_index)]

        new_transitions = prune_none(new_transitions)
        return Result.Ok(FA(
            new_states,
            copy.deepcopy(self.alphabet),
            new_transitions,
            new_initial_state,
            new_final_states
        ))
        
    def __repr__(self):
        """Returns the string representation of the FA."""
        return f"FA(states={self.states}, alphabet={self.alphabet}, transitions={self.transitions}, start_state={self.start_state}, final_states={self.final_states})"


def states_list_from_str(states: list[str]) -> list[State]:
    """Creates a list of states from a list of strings."""
    return [State(int(state[1:])) for state in states]

def symbols_list_from_str(symbols: list[str]) -> list[Symbol]:
    """Creates a list of symbols from a list of strings."""
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
