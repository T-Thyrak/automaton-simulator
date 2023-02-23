from pprint import pformat

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from context import Context

from validate import validate_state_name
from fa import FA, states_list_from_str
from anything import intersection


#** Confirm keyboard and dispatcher **#

def confirm_keyboard(update: Update, context: CallbackContext) -> None:
    """Confirm keyboard."""
    
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data='confirm_yes'),
            InlineKeyboardButton("No", callback_data='confirm_no'),
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def confirm_dispatcher(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    query_text = query.data.split('_')[1]
    did = query_text == 'yes'
    
    if Context.context[update.effective_user.id]['mode'] == 'state_mode_delete':
        output = state_mode_delete_handle_confirm(update, context, did)
        query.edit_message_text(text=output)
        context.bot.send_message(chat_id=update.effective_chat.id, text=state_mode_text(update.effective_user.id), reply_markup=state_mode_keyboard())

#** State mode **#

def state_mode(update: Update, context: CallbackContext) -> None:
    """Handler for state mode."""

    query = update.callback_query
    query.answer()
    
    query.edit_message_text(text=state_mode_text(update.effective_user.id), reply_markup=state_mode_keyboard())
    
def state_mode_text(uid: int) -> str:
    """Prepare the text for state mode."""
    
    return f"Currently in state mode. States = `{pformat(list(map(str, Context.context[uid]['fa'].states)))}`.\nChoose one of the following options:"
    
def state_mode_keyboard() -> InlineKeyboardMarkup:
    """Prepare the state mode keyboard."""
    
    keyboard = [
        [
            InlineKeyboardButton("Add state(s)", callback_data='state_mode_add'),
            InlineKeyboardButton("Delete state(s)", callback_data='state_mode_delete'),
        ],
        [
            InlineKeyboardButton("Back", callback_data='menu'),
        ],
    ]
    
    return InlineKeyboardMarkup(keyboard)

def state_mode_add(update: Update, context: CallbackContext) -> None:
    """Add states to states list."""
    
    query = update.callback_query
    query.answer()
    
    text = f"Enter the states that you want to add, separated by a space.\nAll states must start with the letter 'q' and ends with any amount of numbers. Example: `q0 q1 q2`.\n\nCurrent states: `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].states)))}`"
    
    Context.context[update.effective_user.id]['mode'] = 'state_mode_add'
    
    query.edit_message_text(text=text)
    
def state_mode_add_handle(update: Update, context: CallbackContext) -> str:
    """Handle input from state_mode_add."""
    
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
    
def state_mode_delete(update: Update, context: CallbackContext) -> None:
    """Delete states from the states list."""
    
    query = update.callback_query
    query.answer()
    
    text = f"Enter the states that you want to delete, separated by a space.\nAll states must start with the letter 'q' and ends with any amount of numbers. Example: `q0 q1 q2`.\n\nCurrent states: `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].states)))}`"
    
    Context.context[update.effective_user.id]['mode'] = 'state_mode_delete'
    
    query.edit_message_text(text=text)
    
def state_mode_delete_handle(update: Update, context: CallbackContext) -> None:
    """Handle input from state_mode_delete."""
    
    msg = update.message.text
    states = msg.split()
    
    if not all(map(validate_state_name, states)):
        Context.context[update.effective_user.id]['mode'] = None
        update.message.reply_text("Invalid state name(s). Please try again.")
        update.message.reply_text(text=state_mode_text(update.effective_user.id), reply_markup=state_mode_keyboard())
        return
        
    fa: FA = Context.context[update.effective_user.id]['fa']
    states_s = states_list_from_str(states)
    
    affected_states = intersection(fa.states, states_s, key=lambda s1, s2: s1.id == s2.id)
    if len(affected_states) == 0:
        update.message.reply_text("No states have been deleted.")
        update.message.reply_text(text=state_mode_text(update.effective_user.id), reply_markup=state_mode_keyboard())
        return
    
    Context.context[update.effective_user.id]['tmp']['affected_states'] = affected_states
    
    update.message.reply_text(f"Affected states: `{pformat(list(map(str, affected_states)))}`\n\nAre you sre to delete these states? This action cannot be undone.", reply_markup=confirm_keyboard(update, context))
    
def state_mode_delete_handle_confirm(update: Update, context: CallbackContext, did: bool) -> None:
    """Confirm deletion of states."""
    
    if did:
        fa: FA = Context.context[update.effective_user.id]['fa']
        output = fa.delete_states(Context.context[update.effective_user.id]['tmp']['affected_states'])
        Context.context[update.effective_user.id]['fa'] = fa
        
        if output:
            r = "State(s) have been deleted."
        else:
            r = "No states have been deleted."
    else:
        r = "No states have been deleted."
        
    Context.context[update.effective_user.id]['mode'] = None
    del Context.context[update.effective_user.id]['tmp']['affected_states']
    
    return r

#** Symbol mode **#

def symbol_mode(update: Update, context: CallbackContext) -> None:
    """Handler for symbol mode."""
    
    raise NotImplementedError("symbol_mode")