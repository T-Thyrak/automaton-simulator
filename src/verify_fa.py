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

def verify_fa (fa : FA) -> bool:
    for t in fa.transitions.items():
        # check if symbol contain epsilon
        if t[0][1] == Symbol.epsilon_symbol():
            print('error epsilon')
            return Result.Ok(True)
        # check if to_state have many states
        if len(t[1]) > 1:
            print('error many next states')
            return Result.Ok(True)
    return Result.ok(False)

