import re
from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from pprint import pformat

from context import Context
from fa import FA

# 1.5 Transition
def transition_step(update: Update, context: CallbackContext) -> None:
    """ Handler for transition step"""

    query = update.callback_query
    query.answer()

    query.edit_message_text(text=transition_step_msg(update.effective_user.id), reply_markup=transition_step_button())

def transition_step_msg(uid: int) -> str:
    """ Message for transition"""

    return f"You're in last step of designing FA. \n Click on 1st button to customize transition. \n Click on second button to go to next step.\
        \n\n Current State(s) : `{pformat(list(map(str, Context.context[uid]['fa'].states)))}`.\
        \n Current Symbol : `{pformat(list(map(str, Context.context[uid]['fa'].alphabet)))}`.\
        \n Current Start State: `{str( Context.context[uid]['fa'].start_state)}`.\
        \n Current Final State: `{pformat(list(map(str, Context.context[uid]['fa'].final_states)))}`\
        \n Current Transition: `{Context.context[uid]['fa'].pretty_transition()}`"

def transition_step_button() -> InlineKeyboardMarkup: 
    """ Show State button and Next step button"""

    button = [
        [
            InlineKeyboardButton("5th Step: Transition", callback_data='transition_mode'),
        ],
        [
             InlineKeyboardButton("Back to 4th Step", callback_data='finalstate_step'),
            InlineKeyboardButton("Done Design FA", callback_data='menu'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)

def transition_mode(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    query.edit_message_text(text=transition_mode_msg(update.effective_user.id), reply_markup=transition_mode_button())

def transition_mode_msg(uid: int) -> str:
    """ Message for transition_mode"""
    
    fa: FA = Context.context[uid]['fa']

    return f" You're in the 5th step : Transition Mode. \
           \n Click on any button below.\
            \n\n Current State(s) : `{pformat(list(map(str, Context.context[uid]['fa'].states)))}`.\
           \n Current Symbol : `{pformat(list(map(str, Context.context[uid]['fa'].alphabet)))}`.\
           \n Current Start State: `{str( Context.context[uid]['fa'].start_state)}`.\
           \n Current Final State: `{pformat(list(map(str, Context.context[uid]['fa'].final_states)))}`\
           \n Current Transitions: `{fa.pretty_transition()}`"

def transition_mode_button() -> InlineKeyboardMarkup: 
    """ Show transition button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Add : Transition", callback_data='add_transition_mode'),
            InlineKeyboardButton("Edit : Transition", callback_data='edit_transition_mode'),
            InlineKeyboardButton("Delete : Transition", callback_data='delete_transition_mode'),
            
        ],
        [
            InlineKeyboardButton("Back", callback_data='transition_step'),
        ],
    ]
    
    return InlineKeyboardMarkup(button)

def add_transition_mode(update: Update, context: Context) -> None:
    """Add Transition mode."""
    query = update.callback_query
    query.answer()
    
    text = f" Enter the transition that you want to add (One at a time). \
            \n All states must start with the letter 'q' and ends with any amount of numbers. \
            \n All transitions must be in the format `{{state}}, {{symbol}} => {{states}}`. \
            \n Example: `q0, a => q1, q2`. \
            \n To add epsilon transition, use `eps` as the symbol. \
            \n After you're done, type `/done` to finish adding transitions. \
            \n\n Current State(s) : `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].states)))}`.\
            \n Current Symbol : `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].alphabet)))}`.\
            \n Current Start State: `{str( Context.context[update.effective_user.id]['fa'].start_state)}`.\
            \n Current Final State: `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].final_states)))}`\
            \n Current Transitions: `{Context.context[update.effective_user.id]['fa'].pretty_transition()}`"
            
    Context.context[update.effective_user.id]['mode'] = 'add_transition_mode'
            
    query.edit_message_text(text=text)
    
def add_transition_mode_handle(update: Update, context: Context) -> str:
    """Handle input from add_transition_mode."""
    
    transition = update.message.text
    
    match = re.match(r'^(q\d+)\s?,\s?(\w|eps)\s?=>\s?((?:q\d+\s?,?\s?)+)$', transition)
    
    if not match:
        return "Invalid transition. Please try again."
    
    fa: FA = Context.context[update.effective_user.id]['fa']
    
    from_state = str(match.group(1))
    symbol = str(match.group(2))
    
    to_states_str = match.group(3).split(',')
    to_states = list(map(lambda x: str(x).strip(), to_states_str))
    
    result = fa.add_transition_str(from_state, symbol, to_states)
    
    if result.is_err():
        return f"Invalid transition. Error: {result.unwrap_err()}"
    
    Context.context[update.effective_user.id]['fa'] = fa
    
    has_added = result.unwrap()
    if has_added:
        return f"Transition has been added.\n\nCurrent Transitions: `{fa.pretty_transition()}`"
    else:
        return f"No transition has been added.\n\nCurrent Transitions: `{fa.pretty_transition()}`"
    
def delete_transition_mode(update: Update, context: Context) -> None:
    """Delete Transition mode."""
    
    query = update.callback_query
    query.answer()
    
    text = f" Enter the index of the transition that you want to delete. \
            \n To delete a specific output state, use the format `{{index}}: {{states}}+`. \
            \n Example: `1: q1, q2`. \
            \n Example (no output state, meaning all): `1`. \
            \n\n Current State(s) : `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].states)))}`.\
            \n Current Symbol : `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].alphabet)))}`.\
            \n Current Start State: `{str( Context.context[update.effective_user.id]['fa'].start_state)}`.\
            \n Current Final State: `{pformat(list(map(str, Context.context[update.effective_user.id]['fa'].final_states)))}`\
            \n Current Transitions: `{Context.context[update.effective_user.id]['fa'].pretty_transition(True)}`"
            
    Context.context[update.effective_user.id]['mode'] = 'delete_transition_mode'
            
    query.edit_message_text(text=text)
    
def delete_transition_mode_handle(update: Update, context: Context) -> str:
    """Handle input from delete_transition_mode."""
    
    transition = update.message.text
    
    match = re.match(r'^(\d+)\s?(?::\s?((?:q\d+\s?,?\s?)+))?$', transition)
    
    if not match:
        return "Invalid transition. Please try again."
    
    fa: FA = Context.context[update.effective_user.id]['fa']
    
    index = int(match.group(1).strip()) - 1
    to_states_str = match.group(2)
    
    if to_states_str:
        to_states_str = to_states_str.split(',')
        to_states = list(map(lambda x: str(x).strip(), to_states_str))
    else:
        to_states = None
    
    result = fa.delete_transition_index_str(index, to_states)
    
    if result.is_err():
        return f"Invalid transition. Error: {result.unwrap_err()}"
    
    Context.context[update.effective_user.id]['fa'] = fa
    
    has_deleted = result.unwrap()
    if has_deleted:
        return f"Transition has been deleted.\n\nCurrent Transitions: `{fa.pretty_transition(True)}`"
    else:
        return f"No transition has been deleted.\n\nCurrent Transitions: `{fa.pretty_transition(True)}`"