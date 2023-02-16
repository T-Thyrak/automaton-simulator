import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler

from hello import hello, goodbye

def prepare():
    """Prepare the environment."""
    
    # Load environment variables from .env file
    load_dotenv()

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    
    # simply send a message to the user
    update.message.reply_text(f'Hello {update.effective_user.first_name}!')

def menu(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /menu is issued."""
    
    update.message.reply_text(text=menu_message(), reply_markup=menu_keyboard())
    
def menu_message() -> str:
    """Prepare the menu message."""
    
    return "Choose one of the following options:"

def menu_keyboard() -> InlineKeyboardMarkup:
    """Prepare the menu keyboard."""
    
    keyboard = [
        [
            InlineKeyboardButton("Hello", callback_data='hello'),
            InlineKeyboardButton("Goodbye", callback_data='goodbye'),
        ],
    ]
    
    return InlineKeyboardMarkup(keyboard)

def main() -> None:
    """Main function."""
    prepare()

    # hello world
    token = os.getenv('TG_ACCESS_TOKEN') # get the token from the environment variable
    
    # create the updater
    updater = Updater(token=token, use_context=True)
    
    # add the handler for the /start command
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('menu', menu))
    
    updater.dispatcher.add_handler(CallbackQueryHandler(hello, pattern=r'^hello$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(goodbye, pattern=r'^goodbye$'))
    
    # start the bot
    updater.start_polling()
    
    print("Bot has started!")
    
    # do nothing until we stop the bot
    updater.idle()
    
    print("Bot has stopped!")
    
    pass
    
if __name__ == '__main__':
    main()