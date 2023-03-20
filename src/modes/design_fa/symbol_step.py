from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from pprint import pformat

from validate import validate_symbol
from context import Context
from fa import FA

# 1.2 Symbol Step

def symbol_step(update: Update, context: CallbackContext) -> None:
    """ Handler for state step"""

    query = update.callback_query
    query.answer()

    query.edit_message_text(text=symbol_step_msg(update.effective_user.id), reply_markup=symbol_step_button())

def symbol_step_msg(uid: int) -> str:
    """ Message for symbol"""

    return f" You're in 2nd step of designing FA. \
          \n Click on 1st button to customize symbol. \
          \n Click on 2nd button to go to next step. \
          \n\n Your Current State(s) : `{pformat(list(map(str, Context.context[uid]['fa'].states)))}`.\
          \n Your Current Symbol : `{pformat(list(map(str, Context.context[uid]['fa'].alphabet)))}`."

def symbol_step_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("2nd Step: Symbol", callback_data='symbol_mode'),
        ],
        [   
            InlineKeyboardButton("Back to 1st Step", callback_data='state_step'),
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

    return f" You're in the 2nd step : Symbol Mode. \
           \n Click on any button below.\
           \n\n Your Current State(s) : `{pformat(list(map(str, Context.context[uid]['fa'].states)))}`.\
           \n Your Current Symbol : `{pformat(list(map(str, Context.context[uid]['fa'].alphabet)))}`."

def symbol_mode_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Add : Symbol", callback_data='add_symbol_mode'),
            InlineKeyboardButton("Delete : Symbol", callback_data='delete_symbol_mode'),
            
        ],
        [
            InlineKeyboardButton("Back", callback_data='symbol_step'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)

def add_symbol_mode(update: Update, context: CallbackContext) -> None:
    """Add symbol to symbols list."""

    query = update.callback_query
    query.answer()

    text = f" Enter the symbols that you want to add, separated by a space.\
          \n All symbols will only have one character. \
          \n Example: `a b eps` \
          \n\n Current states: `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].states)))}` \
          \n Current symbols: `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].alphabet)))}`"
    
    Context.context[update.effective_user.id]['mode'] = 'add_symbol_mode'
    print(Context.context[update.effective_user.id]['mode'])
    query.edit_message_text(text=text)

def add_symbol_mode_handle(update: Update, context: CallbackContext) -> str:
    """Handle input from add_symbol_mode."""
    msg = update.message.text
    symbols = msg.split()

    
    if not all(map(validate_symbol, symbols)):
        Context.context[update.effective_user.id]['mode'] = None
        return "Invalid symbol(s). Please try again."

    fa: FA = Context.context[update.effective_user.id]['fa']
    
    has_added = fa.add_symbols_str(symbols)
    
    Context.context[update.effective_user.id]['mode'] = None
    Context.context[update.effective_user.id]['fa'] = fa
    
    if has_added:
        return "Symbol(s) have been added."
    else:
        return "No symbol(s) have been added."

def delete_symbol_mode(update: Update, context: CallbackContext) -> None:
    """Delete states from states list."""
    
    query = update.callback_query
    query.answer()
    
    text = f" Enter the symbols that you want to delete, separated by a space.\
          \n All symbols will only have one character. \
          \n Example: `a b eps` \
          \n\n Current symbols: `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].alphabet)))}` "
    
    Context.context[update.effective_user.id]['mode'] = 'delete_symbol_mode'
    
    query.edit_message_text(text=text)

def delete_symbol_mode_handle(update: Update, context: CallbackContext) -> None:
    """Handle input from delete_symbol_mode."""
    
    msg = update.message.text
    symbols = msg.split()

    if not all(map(validate_symbol, symbols)):
        Context.context[update.effective_user.id]['mode'] = None
        return "Invalid Symbol name(s). Please try again."
    
    fa: FA = Context.context[update.effective_user.id]['fa']
    
    has_deleted = fa.delete_symbol_str(symbols)
    
    Context.context[update.effective_user.id]['mode'] = None
    Context.context[update.effective_user.id]['fa'] = fa
    
    if has_deleted:
        return "Symbol(s) have been deleted."
    else:
        return "No symbol(s) have been deleted."