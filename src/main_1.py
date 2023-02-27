import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from fa import FA, fa_debug as debug, test_debug

from context import Context, unload_context, load_context

from modes_1 import \
        state_step, state_mode ,\
        symbol_step, symbol_mode, \
        startstate_step, startstate_mode, \
        finalstate_step,finalstate_mode, \
        transition_step, transition_mode


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
    
    update.message.reply_text(text=menu_message(), reply_markup=menumode_keyboard())
    
def menu_message() -> str:
    """Prepare the menu message."""
    
    return "Choose one of the following options:"

def menumode_keyboard() -> InlineKeyboardMarkup:
    """Prepare the state mode keyboard."""
    
    keyboard = [
        [
            InlineKeyboardButton("Design FA", callback_data='state_step'),
          
        ],
        [
            InlineKeyboardButton("Back", callback_data='menu'),
        ],
    ]
    
    return InlineKeyboardMarkup(keyboard)

# Menu handler when called from a callback query
def call_menu(update: Update, context: CallbackContext) -> None:
    """Calls the menu."""
    
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(text=menu_message(), reply_markup=menumode_keyboard())


def main() -> None:
    """Main function."""
    prepare()

    # hello world
    token = os.getenv('TG_ACCESS_TOKEN') # get the token from the environment variable
    
    # create the updater
    updater = Updater(token=token, use_context=True)
    
    # add the command handlers, they're the messages that starts with `/`
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('menu', menu))
    

    # navigate to state 
    updater.dispatcher.add_handler(CallbackQueryHandler(state_step, pattern=r'^state_step'))

    updater.dispatcher.add_handler(CallbackQueryHandler(state_mode, pattern=r'^state_mode'))

    # navigate to symbol
    updater.dispatcher.add_handler(CallbackQueryHandler(symbol_step, pattern=r'^symbol_step'))

    updater.dispatcher.add_handler(CallbackQueryHandler(symbol_mode, pattern=r'^symbol_mode$'))
    
    # navigate to start state
    updater.dispatcher.add_handler(CallbackQueryHandler(startstate_step, pattern=r'^startstate_step$'))

    updater.dispatcher.add_handler(CallbackQueryHandler(startstate_mode, pattern=r'^startstate_mode$'))
    
    # navigate to final state
    updater.dispatcher.add_handler(CallbackQueryHandler(finalstate_step, pattern=r'^finalstate_step$'))

    updater.dispatcher.add_handler(CallbackQueryHandler(finalstate_mode, pattern=r'^finalstate_mode$'))

     # navigate to transition
    updater.dispatcher.add_handler(CallbackQueryHandler(transition_step, pattern=r'^transition_step$'))

    updater.dispatcher.add_handler(CallbackQueryHandler(transition_mode, pattern=r'^transition_mode$'))

    # and finally the message handler, it handles all messages
    # here the `~Filters.command` means that we don't want to handle commands
    
    
    # start the bot
    updater.start_polling()
    
    print("Bot has started!")
    
    # do nothing until we stop the bot
    updater.idle()
    
    print("Bot has stopped!")
    
    pass


if __name__ == '__main__':
    Context.context = load_context()
    main()