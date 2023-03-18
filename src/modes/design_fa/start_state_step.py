from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from pprint import pformat

from context import Context
from fa import FA

# 1.3 Start State

def startstate_step(update: Update, context: CallbackContext) -> None:
    """ Handler for state step"""

    query = update.callback_query
    query.answer()

    query.edit_message_text(text=startstate_step_msg(update.effective_user.id), reply_markup=startstate_step_button())

def startstate_step_msg(uid: int) -> str:
    """ Message for State"""

    return f" You're in 3rd step of designing FA. \
            \n Click on 1st button to customize start state. \
            \n Click on second button to go to next step.\
            \n\n Your Current State(s) : `{pformat(list(map(str, Context.context[uid]['fa'].states)))}`.\
            \n Your Current Symbol : `{pformat(list(map(str, Context.context[uid]['fa'].alphabet)))}`.\
            \n Your Current Start State: `{str(Context.context[uid]['fa'].start_state)}`."

def startstate_step_button() -> InlineKeyboardMarkup: 
    """ Show Start State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("3rd Step: Start State", callback_data='startstate_mode'),
        ],
        [
            InlineKeyboardButton("Back to 2nd Step", callback_data='symbol_step'),
            InlineKeyboardButton("Next Step", callback_data='finalstate_step'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)

def startstate_mode(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.answer()

    query.edit_message_text(text=startstate_mode_msg(update.effective_user.id), reply_markup=startstate_mode_button())

def startstate_mode_msg(uid: int) -> str:
    """ Message for Start State_mode"""
    
    return f" You're in the 3rd step : Start State Mode. \
           \n Click on any button below.\
           \n\n Your Current State(s) : `{pformat(list(map(str, Context.context[uid]['fa'].states)))}`.\
            \n Your Current Symbol : `{pformat(list(map(str, Context.context[uid]['fa'].alphabet)))}`.\
            \n Your Current Start State: `{str(Context.context[uid]['fa'].start_state)}`."

def startstate_mode_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Add : Start State", callback_data='add_start_state_mode'),
            InlineKeyboardButton("Edit : Start State", callback_data='edit_startstate_mode'),
            InlineKeyboardButton("Delete : Start State", callback_data='delete_startstate_mode'),
            
        ],
        [
            InlineKeyboardButton("Back", callback_data='startstate_step'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)

def add_start_state_mode(update: Update, context: CallbackContext) -> None:
    """Add states to states list."""
    
    query = update.callback_query
    query.answer()
    
    text = f" Enter the start state that you want to add (Only One state)\
           \n Example: `q0` \
            \n\n Your Current State(s) : `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].states)))}`.\
            \n Your Current Symbol : `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].alphabet)))}`.\
            \n Your Current Start State: `{str(Context.context[update.effective_user.id]['fa'].start_state)}`."
    
    Context.context[update.effective_user.id]['mode'] = 'add_start_state_mode'
    
    query.edit_message_text(text=text)
    # query.edit_message_text(text=)
    
def add_start_state_mode_handle(update: Update, context: CallbackContext) -> str:
    """Handle input from add_state_mode."""
    msg = update.message.text
    start_state = msg.split()
    print(start_state)
    fa: FA = Context.context[update.effective_user.id]['fa']
    
    has_added = fa.add_start_state_str(start_state[0])
    
    Context.context[update.effective_user.id]['mode'] = None
    Context.context[update.effective_user.id]['fa'] = fa
    
    if has_added:
        return f" Start State have been added."
    else:
        return "No state have been added."
    
