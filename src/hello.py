from telegram import Update
from telegram.ext import CallbackContext

def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello, how are you!")