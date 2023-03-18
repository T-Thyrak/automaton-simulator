from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

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