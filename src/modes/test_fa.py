from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from fa import FA
from context import Context
# 3. Test Finite Automaton
def test_step(update: Update, context: CallbackContext) -> None:
    """Handler for test step"""

    query = update.callback_query
    query.answer()

    Context.context[update.effective_user.id]["mode"] = "test_fa"
        
    query.edit_message_text(text=test_step_msg())

def test_step_msg():
    """Message for test step."""
    return "You're in FA testing mode.\n\nEnter a string to test. Once you're done, type `/done` to finish testing."

def test_step_handle(update: Update, context: CallbackContext) -> str:
    """Handle messages during test step."""
    
    string = update.message.text
    fa: FA = Context.context[update.effective_user.id]['fa']
    result = fa.test_accept_str(string)
    if result.is_err():
        return f"Error: {result.unwrap_err()}"
    
    res = result.unwrap()
    
    if res:
        return f"String `{string}` is accepted by the FA."
    else:
        return f"String `{string}` is rejected by the FA."

def test_step_button() -> InlineKeyboardMarkup: 
    """Show test button and Next step button"""

    button = [
        [
            InlineKeyboardButton("Back", callback_data='menu'),
        ],
    ]
    return InlineKeyboardMarkup(button)