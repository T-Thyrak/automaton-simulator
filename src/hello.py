from telegram import Update
from telegram.ext import CallbackContext

def hello(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(text=f'Hello {query.from_user.first_name}!')
    
def goodbye(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f'Goodbye {query.from_user.first_name}!')