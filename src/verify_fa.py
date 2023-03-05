from fa import FA
from state import State
from sym import Symbol
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from context import Context
from result import *

# in fa.transitions.items() 
# t[0] means transitions[(state), (alphabet)]
# t[1] means transitions->to_state
# t[0][1] means transitions->from_state->with_symbol

def verify_fa (fa : FA) -> Result[bool, str]:
    """Verify whether FA is a NFA or DFA.
    
    Args:
        fa (FA): The FA to test
    
    Returns:
        Result[bool, str]: The result of the verification. Ok(true) if NFA, Ok(false) if DFA. Err if undecidable.
    """
    
    if len(fa.transitions) == 0:
        return Result.Err("There is no transitions to check.")
    
    for t in fa.transitions.items():
        # check if symbol contain epsilon
        if t[0][1] == Symbol.epsilon_symbol():
            return Result.Ok(True)
        # check if to_state have many states
        if len(t[1]) > 1:
            return Result.Ok(True)

    return Result.Ok(False)

