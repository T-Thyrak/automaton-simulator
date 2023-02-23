import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from fa import FA, fa_debug as debug, test_debug

from context import Context, unload_context, load_context

from modes import \
    confirm_dispatcher, \
    state_mode, state_mode_text, state_mode_keyboard, state_mode_add, state_mode_add_handle, state_mode_delete, state_mode_delete_handle, \
    symbol_mode
    

#* Context is a singleton class, should not be instantiated
#* Access the context via Context.context
#* The context is simply a dictionary that can hold many things
#* but I've opted to store it like this:
#* {
#*     "fa": FA // the current FA,
#*     "id": Optional[int] // the current FA's id, None if not saved,
#*     "mode": Optional[str] // the current context mode,
#*     "tmp": dict // a temporary dictionary that can be used to store things,
#* }


#** How to handle query **#
#* You always have to answer the query before doing anything:
#* query = update.callback_query
#* query.answer()


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
        
        update.message.reply_text(text="You have not created any FA yet. A new FA has been created for you.")
    
    update.message.reply_text(text=menu_message(), reply_markup=menu_keyboard())
    
def menu_message() -> str:
    """Prepare the menu message."""
    
    return "Choose one of the following options:"

def menu_keyboard() -> InlineKeyboardMarkup:
    """Prepare the menu keyboard."""
    
    keyboard = [
        [
            InlineKeyboardButton("States", callback_data='state_mode'),
            InlineKeyboardButton("Symbol", callback_data='symbol_mode'),
        ],
    ]
    
    return InlineKeyboardMarkup(keyboard)

# Menu handler when called from a callback query
def call_menu(update: Update, context: CallbackContext) -> None:
    """Calls the menu."""
    
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(text=menu_message(), reply_markup=menu_keyboard())

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
    
    Context.context[update.effective_user.id] = {
        "fa": FA.default(),
        "id": None,
        "mode": None,
        "tmp": {}
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
    
    # add the command handlers, they're the messages that starts with `/`
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('menu', menu))
    updater.dispatcher.add_handler(CommandHandler('shutdown_graceful', shutdown_graceful))
    
    updater.dispatcher.add_handler(CommandHandler('newfa', newfa))
    updater.dispatcher.add_handler(CommandHandler('debug', debug))
    updater.dispatcher.add_handler(CommandHandler('test_debug', test_debug))
    
    # add the callback query handlers, they're the messages that starts with `callback_data=` in the keyboard
    updater.dispatcher.add_handler(CallbackQueryHandler(newfa_yes, pattern=r'^newfa_yes$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(newfa_no, pattern=r'^newfa_no$'))
    
    updater.dispatcher.add_handler(CallbackQueryHandler(state_mode, pattern=r'^state_mode$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(state_mode_add, pattern=r'^state_mode_add$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(state_mode_delete, pattern=r'^state_mode_delete$'))
    
    updater.dispatcher.add_handler(CallbackQueryHandler(symbol_mode, pattern=r'^symbol_mode$'))
    
    updater.dispatcher.add_handler(CallbackQueryHandler(confirm_dispatcher, pattern=r'^confirm_.*$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(call_menu, pattern=r'^menu$'))

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
    
    if mode == 'state_mode_add':
        update.message.reply_text(text=state_mode_add_handle(update, context))
        update.message.reply_text(text=state_mode_text(update.effective_user.id), reply_markup=state_mode_keyboard())
    
    if mode == 'state_mode_delete':
        state_mode_delete_handle(update, context)
    else:
        return

# This function is here so we can save the current context
def shutdown_graceful(update: Update, context: CallbackContext) -> None:
    """Cause a graceful shutdown of the bot."""
    
    if update.message.from_user.id != int(os.getenv('TG_ADMIN_ID')):
        update.message.reply_text("You are not authorized to perform this action!")
        return
    
    if len(context.args) != 1:
        update.message.reply_text("You are not authorized to perform this action!")
        return
    
    if context.args[0] != os.getenv('TG_ADMIN_PASSWORD'):
        update.message.reply_text("You are not authorized to perform this action!")
        return
    
    print("A graceful shutdown has been requested by the admin.")
    update.message.reply_text("Shutting down...")
    
    print("Unloading the context... ", end='')
    unload_context(Context.context  )
    print("Done!")
        
    from signal import raise_signal, SIGINT
    raise_signal(SIGINT)

if __name__ == '__main__':
    Context.context = load_context()
    main()