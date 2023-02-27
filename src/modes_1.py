from pprint import pformat

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from context import Context

from validate import validate_state_name
from fa import FA, states_list_from_str
from anything import intersection


def state_step(update: Update, context: CallbackContext) -> None:
    """ Handler for state step"""

    query = update.callback_query
    query.answer()

    query.edit_message_text(text=state_step_msg(update.effective_user.id), reply_markup=state_step_button())

def state_step_msg(uid: int) -> str:
    """ Message for State"""

    return f"You're in 1st step of designing FA. \n Click on 1st button to customize states. \n Click on second button to go to next step."

def state_step_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("1st Step: State", callback_data='state_mode'),
        ],
        [
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

    return f"You're in the 1st step : State mode. \n Click on any button below."

def state_mode_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Add : State", callback_data='add_state_mode'),
            InlineKeyboardButton("Edit : State", callback_data='edit_state_mode'),
            InlineKeyboardButton("Delete : State", callback_data='delete_state_mode'),
            
        ],
        [
            InlineKeyboardButton("Back", callback_data='state_step'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)


def symbol_step(update: Update, context: CallbackContext) -> None:
    """ Handler for state step"""

    query = update.callback_query
    query.answer()

    query.edit_message_text(text=symbol_step_msg(update.effective_user.id), reply_markup=symbol_step_button())

def symbol_step_msg(uid: int) -> str:
    """ Message for symbol"""

    return f"You're in 2nd step of designing FA. \n Click on 1st button to customize symbol. \n Click on second button to go to next step."

def symbol_step_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("2nd Step: Symbol", callback_data='symbol_mode'),
        ],
        [
            InlineKeyboardButton("Next Step", callback_data='startstate_step'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)

def symbol_mode(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.answer()

    query.edit_message_text(text=symbol_mode_msg(update.effective_user.id), reply_markup=symbol_mode_button())

def symbol_mode_msg(uid: int) -> str:
    """ Message for symbol_mode"""

    return f"You're in the 2nd step : Symbol mode. \n Click on any button below."

def symbol_mode_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Add : Symbol", callback_data='add_symbol_mode'),
            InlineKeyboardButton("Edit : Symbol", callback_data='edit_symbol_mode'),
            InlineKeyboardButton("Delete : Symbol", callback_data='delete_symbol_mode'),
            
        ],
        [
            InlineKeyboardButton("Back", callback_data='symbol_step'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)

def startstate_step(update: Update, context: CallbackContext) -> None:
    """ Handler for state step"""

    query = update.callback_query
    query.answer()

    query.edit_message_text(text=startstate_step_msg(update.effective_user.id), reply_markup=startstate_step_button())

def startstate_step_msg(uid: int) -> str:
    """ Message for State"""

    return f"You're in 3rd step of designing FA. \n Click on 1st button to customize start state. \n Click on second button to go to next step."

def startstate_step_button() -> InlineKeyboardMarkup: 
    """ Show Start State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("3rd Step: Start State", callback_data='startstate_mode'),
        ],
        [
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

    return f"You're in the 3rd step : Start State mode. \n Click on any button below."

def startstate_mode_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Add : Start State", callback_data='add_startstate_mode'),
            InlineKeyboardButton("Edit : Start State", callback_data='edit_startstate_mode'),
            InlineKeyboardButton("Delete : Start State", callback_data='delete_startstate_mode'),
            
        ],
        [
            InlineKeyboardButton("Back", callback_data='startstate_step'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)


def finalstate_step(update: Update, context: CallbackContext) -> None:
    """ Handler for state step"""

    query = update.callback_query
    query.answer()

    query.edit_message_text(text=finalstate_step_msg(update.effective_user.id), reply_markup=finalstate_step_button())

def finalstate_step_msg(uid: int) -> str:
    """ Message for final state"""

    return f"You're in 4th step of designing FA. \n Click on 1st button to customize final state. \n Click on second button to go to next step."

def finalstate_step_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("4th Step: Final State", callback_data='finalstate_mode'),
        ],
        [
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

    return f"You're in the 4th step : Final State Mode. \n Click on any button below."

def finalstate_mode_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Add : Final State", callback_data='add_finalstate_mode'),
            InlineKeyboardButton("Edit : Final State", callback_data='edit_finalstate_mode'),
            InlineKeyboardButton("Delete : Final State", callback_data='delete_finalstate_mode'),
            
        ],
        [
            InlineKeyboardButton("Back", callback_data='finalstate_step'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)