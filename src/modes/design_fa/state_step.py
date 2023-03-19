from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from pprint import pformat

from validate import validate_state_name
from context import Context
from fa import FA

# 1. Design Finite Automaton
# 1.1 State Step
def state_step(update: Update, context: CallbackContext) -> None:
    """ Handler for state step"""

    query = update.callback_query
    query.answer()

    query.edit_message_text(text=state_step_msg(update.effective_user.id), reply_markup=state_step_button())

def state_step_msg(uid: int) -> str:
    """ Message for State"""

    return f" You're in 1st step of designing FA. \
           \n Click on 1st button to customize states. \
           \n Click on second button to go to next step.\
           \n\n Your Current State(s) : `{pformat(list(map(str, Context.context[uid]['fa'].states)))}`."

def state_step_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("1st Step: State", callback_data='state_mode'),
        ],
        [
            InlineKeyboardButton("Back to Menu", callback_data='menu'),
            InlineKeyboardButton("Next Step", callback_data='symbol_step'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)

def state_mode(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.answer()

    query.edit_message_text(text=state_mode_msg(update.effective_user.id), reply_markup=state_mode_button())

def state_mode_msg(uid: int) -> str:
    """ Message for State_mode"""

    return f" You're in the 1st step : State Mode. \
           \n Click on any button below. \
           \n\n Your Current State(s) : `{pformat(list(map(str, Context.context[uid]['fa'].states)))}`."

def state_mode_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Add : State(s)", callback_data='add_state_mode'),
            InlineKeyboardButton("Edit : State(s)", callback_data='edit_state_mode'),
            InlineKeyboardButton("Delete : State(s)", callback_data='delete_state_mode'),
            
        ],
        [
            InlineKeyboardButton("Back", callback_data='state_step'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)

def add_state_mode(update: Update, context: CallbackContext) -> None:
    """Add states to states list."""
    
    query = update.callback_query
    query.answer()
    
    text = f" Enter the states that you want to add, separated by a space.\
          \n All states must start with the letter 'q' and ends with any amount of numbers. \
          \n Example: `q0 q1 q2`.\
          \n\n Current states: `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].states)))}`"
    
    Context.context[update.effective_user.id]['mode'] = 'add_state_mode'
    
    query.edit_message_text(text=text)
    
def add_state_mode_handle(update: Update, context: CallbackContext) -> str:
    """Handle input from add_state_mode."""
    
    msg = update.message.text
    states = msg.split()

    if not all(map(validate_state_name, states)):
        Context.context[update.effective_user.id]['mode'] = None
        return "Invalid state name(s). Please try again."
    
    fa: FA = Context.context[update.effective_user.id]['fa']
    
    has_added = fa.add_states_str(states)
    
    Context.context[update.effective_user.id]['mode'] = None
    Context.context[update.effective_user.id]['fa'] = fa
    
    if has_added:
        return "State(s) have been added."
    else:
        return "No state(s) have been added."
    
def delete_state_mode(update: Update, context: CallbackContext) -> None:
    """Delete states from states list."""
    
    query = update.callback_query
    query.answer()
    
    text = f" Enter the states that you want to delete, separated by a space.\
          \n All states must start with the letter 'q' and ends with any amount of numbers. \
          \n Example: `q0 q1 q2`.\
          \n\n Current states: `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].states)))}`"
    
    Context.context[update.effective_user.id]['mode'] = 'delete_state_mode'
    
    query.edit_message_text(text=text)
    
def delete_state_mode_handle(update: Update, context: CallbackContext) -> None:
    """Handle input from delete_state_mode."""
    
    msg = update.message.text
    states = msg.split()

    if not all(map(validate_state_name, states)):
        Context.context[update.effective_user.id]['mode'] = None
        return "Invalid state name(s). Please try again."
    
    fa: FA = Context.context[update.effective_user.id]['fa']
    
    has_deleted = fa.delete_states_str(states)
    
    Context.context[update.effective_user.id]['mode'] = None
    Context.context[update.effective_user.id]['fa'] = fa
    
    if has_deleted:
        return "State(s) have been deleted."
    else:
        return "No state(s) have been deleted."