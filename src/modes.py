import re

from pprint import pformat

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from context import Context
from state import State
from sym import Symbol

from validate import validate_state_name, validate_symbol
from fa import FA, start_state_list_from_str, states_list_from_str
from anything import intersection

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
            InlineKeyboardButton("Edit : Symbol", callback_data='edit_symbol_mode'),
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
            InlineKeyboardButton("Next Step", callback_data='transition_step'),
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

    return f"You're in the 5th step : Transition Mode. \n Click on any button below.\n\nTransitions: `{fa.pretty_transition()}`"

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
            \n\n Current Transitions: `{Context.context[update.effective_user.id]['fa'].pretty_transition()}`"
            
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
            \n\n Current Transitions: `{Context.context[update.effective_user.id]['fa'].pretty_transition(True)}`"
            
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

# 2. Verify Finite Automaton
def verify_step(update: Update, context: CallbackContext) -> None:
    """ Handler for state step"""

    query = update.callback_query
    query.answer()

    query.edit_message_text("Under Construction", reply_markup=verify_step_button())

def verify_step_button() -> InlineKeyboardMarkup: 
    """ Show Verify button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Back", callback_data='menu'),
        ],
    ]
    return InlineKeyboardMarkup(button)

# 3. Test Finite Automaton
def test_step(update: Update, context: CallbackContext) -> None:
    """ Handler for test step"""

    query = update.callback_query
    query.answer()

    query.edit_message_text("Under Construction", reply_markup=test_step_button())

def test_step_button() -> InlineKeyboardMarkup: 
    """ Show test button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Back", callback_data='menu'),
        ],
    ]
    return InlineKeyboardMarkup(button)

# 4. Determinization Finite Automaton
def det_step(update: Update, context: CallbackContext) -> None:
    """ Handler for state step"""

    query = update.callback_query
    query.answer()

    query.edit_message_text("Under Construction", reply_markup=det_step_button())

def det_step_button() -> InlineKeyboardMarkup: 
    """ Show Determinization button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Back", callback_data='menu'),
        ],
    ]
    return InlineKeyboardMarkup(button)

# 5. Verify Finite Automaton
def min_step(update: Update, context: CallbackContext) -> None:
    """ Handler for Minimization step"""

    query = update.callback_query
    query.answer()

    query.edit_message_text("Under Construction", reply_markup=min_step_button())

def min_step_button() -> InlineKeyboardMarkup: 
    """ Show Verify button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Back", callback_data='menu'),
        ],
    ]
    return InlineKeyboardMarkup(button)