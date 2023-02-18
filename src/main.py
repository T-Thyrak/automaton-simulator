import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler

from hello import hello, goodbye
from fa import FA

from context import context as context_mappings

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

def newfa(update: Update, context: CallbackContext) -> None:
    """Creates a new FA."""
    
    update.message.reply_text(text=newfa_message(), reply_markup=newfa_keyboard())
    
def newfa_message() -> str:
    """Prepare the new FA message."""
    
    return "Are you sure to create a new FA? You may have unsaved changes."

def newfa_keyboard() -> InlineKeyboardMarkup:
    """Prepare the new FA keyboard."""
    
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data='newfa_yes'),
            InlineKeyboardButton("No", callback_data='newfa_no'),
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def newfa_yes(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    context_mappings[update.effective_user.id] = {
        "fa": FA.default(),
        "id": None,
    }
    
    query.edit_message_text(text="New FA created!")
    
def newfa_no(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(text="New FA creation cancelled!")

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
    updater.dispatcher.add_handler(CommandHandler('shutdown_graceful', shutdown_graceful))
    
    updater.dispatcher.add_handler(CommandHandler('newfa', newfa))
    
    updater.dispatcher.add_handler(CallbackQueryHandler(newfa_yes, pattern=r'^newfa_yes$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(newfa_no, pattern=r'^newfa_no$'))
    
    updater.dispatcher.add_handler(CallbackQueryHandler(hello, pattern=r'^hello$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(goodbye, pattern=r'^goodbye$'))
    
    # start the bot
    updater.start_polling()
    
    print("Bot has started!")
    
    # do nothing until we stop the bot
    updater.idle()
    
    print("Bot has stopped!")
    
    pass

def shutdown_graceful(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != int(os.getenv('TG_ADMIN_ID')):
        update.message.reply_text("You are not authorized to perform this action!")
        return
    
    if len(context.args) != 1:
        update.message.reply_text("You are not authorized to perform this action!")
        return
    
    if context.args[0] != os.getenv('TG_ADMIN_PASSWORD'):
        update.message.reply_text("You are not authorized to perform this action!")
        return
    
    update.message.reply_text("Shutting down...")
    
    from signal import raise_signal, SIGINT
    raise_signal(SIGINT)        

if __name__ == '__main__':
    main()