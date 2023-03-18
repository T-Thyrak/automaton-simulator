from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from context import Context
from fa import FA

# 2. Verify Finite Automaton
def verify_step(update: Update, context: CallbackContext) -> None:
    """ Handler for state step"""

    query = update.callback_query
    query.answer()

    header = "You're in Verify FA.\n\n"
    fa: FA = Context.context[update.effective_user.id]['fa']
    result = fa.verify_fa()

    if result.is_err():
        text = f"Cannot decide: Error: {result.unwrap_err()}"
    else:
        res = result.unwrap()
        if res:
            text = header + "FA that you have been designed is NFA."
        else:
            text = header + "FA that you have been designed is DFA."

    query.edit_message_text(text=text, reply_markup=verify_step_button())

def verify_step_button() -> InlineKeyboardMarkup: 
    """ Show Verify button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Back to Menu", callback_data='menu'),
        ],
    ]
    return InlineKeyboardMarkup(button)