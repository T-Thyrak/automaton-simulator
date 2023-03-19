from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from pprint import pformat

from validate import validate_state_name
from context import Context
from fa import FA


# 1.4 Final State

def finalstate_step(update: Update, context: CallbackContext) -> None:
    """ Handler for state step"""

    query = update.callback_query
    query.answer()

    query.edit_message_text(text=finalstate_step_msg(update.effective_user.id), reply_markup=finalstate_step_button())

def finalstate_step_msg(uid: int) -> str:
    """ Message for final state"""

    return f" You're in 4th step of designing FA. \
          \n Click on 1st button to customize final state.\
           \n Click on second button to go to next step.\
            \n\n Your Current State(s) : `{pformat(list(map(str, Context.context[uid]['fa'].states)))}`.\
            \n Your Current Symbol : `{pformat(list(map(str, Context.context[uid]['fa'].alphabet)))}`.\
            \n Your Current Start State: `{str( Context.context[uid]['fa'].start_state)}`.\
           \n Your Current Final State: `{pformat(list(map(str, Context.context[uid]['fa'].final_states)))}`"

def finalstate_step_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("4th Step: Final State", callback_data='finalstate_mode'),
        ],
        [
            InlineKeyboardButton("Back to 3rd Step", callback_data='startstate_step'),
            InlineKeyboardButton("Next Step", callback_data='transition_step'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)

def finalstate_mode(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.answer()

    query.edit_message_text(text=finalstate_mode_msg(update.effective_user.id), reply_markup=finalstate_mode_button())

def finalstate_mode_msg(uid: int) -> str:
    """ Message for symbol_mode"""
    return f"You're in the 4th step : Final State Mode. \
          \n Click on any button below.\
           \n\n Your Current State(s) : `{pformat(list(map(str, Context.context[uid]['fa'].states)))}`.\
            \n Your Current Symbol : `{pformat(list(map(str, Context.context[uid]['fa'].alphabet)))}`.\
            \n Your Current Start State: `{str( Context.context[uid]['fa'].start_state)}`.\
           \n Your Current Final States: `{pformat(list(map(str, Context.context[uid]['fa'].final_states)))}`"

def finalstate_mode_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Add : Final State", callback_data='add_final_states_mode'),
            InlineKeyboardButton("Edit : Final State", callback_data='edit_finalstate_mode'),
            InlineKeyboardButton("Delete : Final State", callback_data='delete_finalstate_mode'),
            
        ],
        [
            InlineKeyboardButton("Back", callback_data='finalstate_step'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)
def add_final_states_mode(update: Update, context: CallbackContext) -> None:
    """Add states to states list."""
    
    query = update.callback_query
    query.answer()
    
    text = f" Enter the final states that you want to add, separated by a space.\
          \n All states must start with the letter 'q' and ends with any amount of numbers. \
          \n Example: `q0 q1 q2`.\
           \n\n Your Current State(s) : `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].states)))}`.\
            \n Your Current Symbol : `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].alphabet)))}`.\
            \n Your Current Start State: `{str( Context.context[update.effective_user.id]['fa'].start_state)}`.\
            \n Your Current Final States: `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].final_states)))}`"
    
    Context.context[update.effective_user.id]['mode'] = 'add_final_states_mode'
    
    query.edit_message_text(text=text)
    
def add_final_states_mode_handle(update: Update, context: CallbackContext) -> str:
    """Handle input from add_state_mode."""
    
    msg = update.message.text
    final_states = msg.split()

    if not all(map(validate_state_name, final_states)):
        Context.context[update.effective_user.id]['mode'] = None
        return "Invalid state name(s). Please try again."
    
    fa: FA = Context.context[update.effective_user.id]['fa']
    
    has_added = fa.add_final_states_str(final_states)
    
    Context.context[update.effective_user.id]['mode'] = None
    Context.context[update.effective_user.id]['fa'] = fa
    
    if has_added:
        return f"Final State(s) have been added."
    else:
        return "No state(s) have been added."