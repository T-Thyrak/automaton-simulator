from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from pprint import pformat

from context import Context
from fa import FA
from saveload import go_save, go_save_new, go_load, show_saved_fa, is_valid_id

# Save step
def save_step(update: Update, context: CallbackContext) -> None:
    """Handler for Saving or Loading step"""
    
    query = update.callback_query
    query.answer()
    
    if Context.context.get(update.effective_user.id) is None:
        Context.context[update.effective_user.id] = {
            'fa': FA.default(),
            'id': None,
            'mode': None,
            'tmp': {}
        }
        
        update.message.reply_text("You don't have any FA created yet, so I created one for you.")
    
    query.edit_message_text(text=save_step_msg(update.effective_user.id), reply_markup=save_step_button())
    
def save_step_msg(uid: int) -> str:
    """Prepare message for Saving or Loading step"""
    
    fa: FA = Context.context[uid]['fa']
    Context.context[uid]['mode'] = None
    
    return f"You're currently in saving/loading mode. \
            \n Current ID: `{Context.context[uid]['id']}`.\
            \n\n Current State(s) : `{pformat(list(map(str, fa.states)))}`.\
            \n Current Symbol : `{pformat(list(map(str, fa.alphabet)))}`.\
            \n Current Start State: `{str(fa.start_state)}`.\
            \n Current Final State: `{pformat(list(map(str, fa.final_states)))}`\
            \n Current Transitions: `{fa.pretty_transition()}`"
            
def save_step_button() -> InlineKeyboardMarkup:
    """Show Saving or Loading button"""
    
    button = [
        [
            InlineKeyboardButton("Save", callback_data='save'),
            InlineKeyboardButton("Save as new", callback_data='new_save'),
            InlineKeyboardButton("Load", callback_data='load'),
        ],
        [
            InlineKeyboardButton("Back", callback_data='menu'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)

def just_back() -> InlineKeyboardMarkup:
    """Just a back button."""
    
    button = [
        [
            InlineKeyboardButton("Back", callback_data='save_step'),
        ]
    ]
    
    return InlineKeyboardMarkup(button)

def save(update: Update, context: CallbackContext) -> None:
    """Handler for saving the FA."""
    
    query = update.callback_query
    query.answer()
    
    fa: FA = Context.context[update.effective_user.id]['fa']
    
    result = go_save(fa, update.effective_user.id, Context.context[update.effective_user.id]['id'])
    
    if result.is_err():
        query.edit_message_text(text=f"Couldn't save. Error: {result.unwrap_err()}", reply_markup=just_back())
    
    fa_id = result.unwrap()
    
    Context.context[update.effective_user.id]['id'] = fa_id
    
    query.edit_message_text(text=f"Saved successfully. ID: {fa_id}", reply_markup=just_back())
    
def save_new(update: Update, context: CallbackContext) -> None:
    """Handler for saving the FA as a new record."""
    
    query = update.callback_query
    query.answer()
    
    fa: FA = Context.context[update.effective_user.id].get('fa')
    
    if fa is None:
        query.edit_message_text(text=f"Couldn't save. Error: No FA is designed yet.", reply_markup=just_back())
        return
    
    result = go_save_new(fa, update.effective_user.id)
    
    if result.is_err():
        query.edit_message_text(text=f"Couldn't save. Error: {result.unwrap_err()}", reply_markup=just_back())
        
    fa_id = result.unwrap()
    
    Context.context[update.effective_user.id]['id'] = fa_id
    
    query.edit_message_text(text=f"Saved successfully. ID: {fa_id}", reply_markup=just_back())
    
def load(update: Update, context: CallbackContext) -> None:
    """Handler for loading the FA."""
    
    query = update.callback_query
    query.answer()

    Context.context[update.effective_user.id]['mode'] = 'load_mode'
    
    fas = show_saved_fa(update.effective_user.id)
    if fas.is_err():
        query.edit_message_text(text=f"Couldn't load. Error: {fas.unwrap_err()}")
        return
    
    text = f"Please type the ID of the FA that you want to load. Saved FA(s): `{pformat(fas.unwrap())}`"
    
    query.edit_message_text(text=text, reply_markup=just_back())
    
def load_mode_handle(update: Update, context: CallbackContext) -> str:
    """Handler for loading the FA after the user has inputted."""
    
    Context.context[update.effective_user.id]['mode'] = None
    
    fa_id = update.message.text
    real_fa_id = fa_id.strip()
    
    # validate that the input is a number
    if not real_fa_id.isnumeric():
        return "Please input a number."
    
    # validate that the input is a valid ID
    if not is_valid_id(update.effective_user.id, real_fa_id):
        return "Please input a valid ID."

    # Load the FA
    
    result = go_load(update.effective_user.id, real_fa_id)
    
    if result.is_err():
        return f"Couldn't load. Error: {result.unwrap_err()}"
    
    fa = result.unwrap()
    
    if fa is None:
        return f"Couldn't load. Error: Failed while parsing the FA."
    
    Context.context[update.effective_user.id]['fa'] = fa
    Context.context[update.effective_user.id]['id'] = int(real_fa_id)
    
    return f"Loaded successfully. ID: {real_fa_id}"