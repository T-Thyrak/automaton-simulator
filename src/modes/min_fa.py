from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from pprint import pformat

from fa import FA
from context import Context

# 5. Verify Finite Automaton
def min_step(update: Update, context: CallbackContext) -> None:
    """ Handler for Minimization step"""

    query = update.callback_query
    query.answer()
    
    fa: FA = Context.context[update.effective_user.id].get('fa')
    if fa is None:
        query.edit_message_text("You haven't created any FA yet. Please create one first.", reply_markup=min_step_button())
        return

    result = fa.minimize()
    if result.is_err():
        query.edit_message_text(f"Minimizing Error: {result.unwrap_err()}", reply_markup=min_step_button())
    
    fa = result.unwrap()
    Context.context[update.effective_user.id]['fa'] = fa

    query.edit_message_text(f"Minimizing FA successful. \
            \n\nCurrent States: `{pformat(list(map(str, fa.states)))}`\
            \nCurrent Symbol: `{pformat(list(map(str, fa.alphabet)))}`\
            \nCurrent Start State: `{str(fa.start_state)}`\
            \nCurrent Final State: `{pformat(list(map(str, fa.final_states)))}`\
            \nCurrent Transitions: `{fa.pretty_transition()}`", reply_markup=min_step_button())

def min_step_button() -> InlineKeyboardMarkup: 
    """ Show Verify button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Back", callback_data='menu'),
        ],
    ]
    return InlineKeyboardMarkup(button)