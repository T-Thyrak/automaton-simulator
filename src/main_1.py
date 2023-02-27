import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from fa import FA, fa_debug as debug, test_debug


from context import Context, unload_context, load_context

from modes_1 import \
        state_step, state_mode ,state_mode_msg,state_mode_button,add_state_mode_handle,add_state_mode,\
        symbol_step, symbol_mode, \
        startstate_step, startstate_mode, \
        finalstate_step,finalstate_mode, \
        transition_step, transition_mode,\
        verify_step,test_step,det_step,min_step


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
    
    # Create a new FA if the user has not created any FA yet
    if Context.context.get(update.effective_user.id) is None:
        Context.context[update.effective_user.id] = {
            "fa": FA.default(),
            "id": None,
            "mode": None,
            "tmp": {},
        }

    update.message.reply_text(text=menu_message(), reply_markup=menumode_keyboard())
    
def menu_message() -> str:
    """Prepare the menu message."""
    
    return "Choose one of the following options:"

def menumode_keyboard() -> InlineKeyboardMarkup:
    """Prepare the state mode keyboard."""
    
    keyboard = [
        [
            InlineKeyboardButton("Design FA", callback_data='state_step'),
            InlineKeyboardButton("Verify FA", callback_data='verify_step'),
            InlineKeyboardButton("Test String", callback_data='test_step'),
        ],
        [
            InlineKeyboardButton("Determinization", callback_data='det_step'),
            InlineKeyboardButton("Minimization", callback_data='min_step'),
          
        ],
        [
            InlineKeyboardButton("Done", callback_data='done'),
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
    updater.dispatcher.add_handler(CallbackQueryHandler(state_step, pattern=r'^state_step$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(state_mode, pattern=r'^state_mode$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(add_state_mode, pattern=r'^add_state_mode$'))

    # navigate to symbol
    updater.dispatcher.add_handler(CallbackQueryHandler(symbol_step, pattern=r'^symbol_step$'))
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

    # navigate to verify finite automata
    updater.dispatcher.add_handler(CallbackQueryHandler(verify_step, pattern=r'^verify_step$'))

    # navigate to test finite automata
    updater.dispatcher.add_handler(CallbackQueryHandler(test_step, pattern=r'^test_step$'))

    # navigate to determinization
    updater.dispatcher.add_handler(CallbackQueryHandler(det_step, pattern=r'^det_step$'))

    # navigate to minimization
    updater.dispatcher.add_handler(CallbackQueryHandler(min_step, pattern=r'^min_step$'))

    # and finally the message handler, it handles all messages
    # here the `~Filters.command` means that we don't want to handle commands
    updater.dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command,
        message_handler
    ))
    
    
    # start the bot
    updater.start_polling()
    
    print("Bot has started!")
    
    # do nothing until we stop the bot
    updater.idle()
    
    print("Bot has stopped!")
    
    pass

def message_handler(update: Update, context: CallbackContext) -> None:
    """Handle straight messages."""
    
    if Context.context.get(update.effective_user.id) is None:
        return
    
    mode = Context.context[update.effective_user.id]['mode']
    
    # Update state(s) if the and show state mode displayer
    if mode == 'add_state_mode':
        update.message.reply_text(text=add_state_mode_handle(update, context))
        update.message.reply_text(text=state_mode_msg(update.effective_user.id), reply_markup=state_mode_button())
    else:
        return

if __name__ == '__main__':
    Context.context = load_context()
    main()