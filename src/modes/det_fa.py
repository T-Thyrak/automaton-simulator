from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from pprint import pformat

from fa import FA
from context import Context

# 4. Determinization Finite Automaton
def det_step(update: Update, context: CallbackContext) -> None:
    """ Handler for state step"""

    query = update.callback_query
    query.answer()

    fa: FA = Context.context[update.effective_user.id].get('fa')
    if fa is None:
        query.edit_message_text(text="You haven't create any FA yet. Please create on first.", reply_markup=det_step_button())
        return
    
    result = fa.determinize()
    if result.is_err():
        query.edit_message_text(text=f"Determinization Error: {result.unwrap_err()}", reply_markup=det_step_button())
        return
    
    fa = result.unwrap()
    Context.context[update.effective_user.id]['fa'] = fa
    
    query.edit_message_text(f"Determinization FA successful. \
            \n\nCurrent States: `{pformat(list(map(str, fa.states)))}`\
            \nCurrent Symbol: `{pformat(list(map(str, fa.alphabet)))}`\
            \nCurrent Start State: `{str(fa.start_state)}`\
            \nCurrent Final State: `{pformat(list(map(str, fa.final_states)))}`\
            \nCurrent Transitions: `{fa.pretty_transition()}`", reply_markup=det_step_button())

def det_step_button() -> InlineKeyboardMarkup: 
    """ Show Determinization button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Back", callback_data='menu'),
        ],
    ]
    return InlineKeyboardMarkup(button)