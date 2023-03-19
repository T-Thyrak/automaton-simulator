from ext.console import CONSOLE

import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from fa import FA, fa_debug as debug

from context import Context, unload_context, load_context

from menu import menu, call_menu, menu_message, menumode_keyboard

# from modes import \
#         state_step, state_mode ,state_mode_msg,state_mode_button,add_state_mode_handle,add_state_mode, delete_state_mode_handle, delete_state_mode, \
#         symbol_step, symbol_mode, add_symbol_mode, add_symbol_mode_handle, symbol_mode_button, symbol_mode_msg, \
#         startstate_step, startstate_mode, startstate_mode_msg, startstate_mode_button, add_start_state_mode_handle,add_start_state_mode,\
#         finalstate_step,finalstate_mode, finalstate_mode_msg, finalstate_mode_button, add_final_states_mode_handle,add_final_states_mode, \
#         transition_step, transition_mode, transition_mode_msg, transition_mode_button, add_transition_mode_handle, add_transition_mode, delete_transition_mode_handle, delete_transition_mode, \
#         verify_step,test_step,det_step,min_step, save_step, save, load, load_mode_handle, just_back

from modes.design_fa.state_step import state_step, state_mode, add_state_mode, \
    add_state_mode_handle, delete_state_mode, delete_state_mode_handle, state_mode_msg, state_mode_button
from modes.design_fa.symbol_step import symbol_step, symbol_mode, add_symbol_mode, \
    add_symbol_mode_handle, symbol_mode_button, symbol_mode_msg
from modes.design_fa.start_state_step import startstate_step, startstate_mode, add_start_state_mode, \
    add_start_state_mode_handle, startstate_mode_msg, startstate_mode_button
from modes.design_fa.final_states_step import finalstate_step, finalstate_mode, add_final_states_mode, \
    add_final_states_mode_handle, finalstate_mode_msg, finalstate_mode_button
from modes.design_fa.transition_step import transition_step, transition_mode, add_transition_mode, \
    add_transition_mode_handle, delete_transition_mode, delete_transition_mode_handle, \
    transition_mode_msg, transition_mode_button
from modes.verify_fa import verify_step
from modes.test_fa import test_step, test_step_handle
from modes.det_fa import det_step
from modes.min_fa import min_step
from modes.save_load_fa import save_step, save, save_new, load, load_mode_handle, just_back

from modes import \
        state_step, state_mode ,state_mode_msg,state_mode_button,add_state_mode_handle,add_state_mode, delete_state_mode_handle, delete_state_mode, \
        symbol_step, symbol_mode, add_symbol_mode, add_symbol_mode_handle, symbol_mode_button, symbol_mode_msg,delete_symbol_mode_handle,  delete_symbol_mode, \
        startstate_step, startstate_mode, startstate_mode_msg, startstate_mode_button, add_start_state_mode_handle,add_start_state_mode,delete_start_state_mode, detete_start_state_mode_handle,\
        finalstate_step,finalstate_mode, finalstate_mode_msg, finalstate_mode_button, add_final_states_mode_handle, add_final_states_mode, delete_final_states_mode_handle, delete_final_states_mode,\
        transition_step, transition_mode, transition_mode_msg, transition_mode_button, add_transition_mode_handle, add_transition_mode, delete_transition_mode_handle, delete_transition_mode, \
        verify_step,test_string_step,det_step,min_step, test_string_handle, test_string_step_button


def prepare():
    """Prepare the environment."""
    
    # Load environment variables from .env file
    load_dotenv()

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    
    # simply send a message to the user
    update.message.reply_text(f'Hello {update.effective_user.first_name}!')


# Done handler when called from a callback query
def done(update: Update, context: CallbackContext) -> None:
    """Done handler."""
    
    if Context.context.get(update.effective_user.id) is None:
        return
    
    if Context.context[update.effective_user.id]['mode'] not in [
        "add_transition_mode",
        "delete_transition_mode",
        "test_fa"
    ]:
        return
    
    if Context.context[update.effective_user.id]['id'] in [
        "add_transition_mode",
        "delete_transition_mode"
    ]:
        Context.context[update.effective_user.id]['id'] = None
        update.message.reply_text(text=transition_mode_msg(update.effective_user.id), reply_markup=transition_mode_button())
        return
    
    if Context.context[update.effective_user.id]['id'] == "test_fa":
        Context.context[update.effective_user.id]['id'] = None
        update.message.reply_text(text=menu_message(), reply_markup=menumode_keyboard())
        return

def reset(update: Update, context: CallbackContext) -> None:
    if Context.context.get(update.effective_user.id) is None:
        Context.context[update.effective_user.id] = {
            'fa': FA.default(),
            'id': None,
            'mode': None,
            'tmp': {}
        }

        update.message.reply_text("You have not created any FA yet, so a default one has been created.")
        return

    Context.context[update.effective_user.id]['fa'] = FA.default()
    Context.context[update.effective_user.id]['id'] = None

def main() -> None:
    """Main function."""
    prepare()

    # hello world
    token = os.getenv('TG_ACCESS_TOKEN') # get the token from the environment variable
    
    # create the updater
    updater = Updater(token=token, use_context=True)
    
    # add the command handlers, they're the messages that starts with /
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('menu', menu))
    updater.dispatcher.add_handler(CommandHandler('done', done))
    updater.dispatcher.add_handler(CommandHandler('reset', reset))
    updater.dispatcher.add_handler(CommandHandler('debug', debug))

    updater.dispatcher.add_handler(CallbackQueryHandler(call_menu, pattern=r"^menu$"))
    # navigate to state 
    updater.dispatcher.add_handler(CallbackQueryHandler(state_step, pattern=r'^state_step$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(state_mode, pattern=r'^state_mode$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(add_state_mode, pattern=r'^add_state_mode$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(delete_state_mode, pattern=r'^delete_state_mode$'))

    # navigate to symbol
    updater.dispatcher.add_handler(CallbackQueryHandler(symbol_step, pattern=r'^symbol_step$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(symbol_mode, pattern=r'^symbol_mode$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(add_symbol_mode, pattern=r'^add_symbol_mode$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(delete_symbol_mode, pattern=r'^delete_symbol_mode$'))

    # navigate to start state
    updater.dispatcher.add_handler(CallbackQueryHandler(startstate_step, pattern=r'^startstate_step$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(startstate_mode, pattern=r'^startstate_mode$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(add_start_state_mode, pattern=r'^add_start_state_mode$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(delete_start_state_mode, pattern=r'delete_start_state_mode$'))

    
    # navigate to final state
    updater.dispatcher.add_handler(CallbackQueryHandler(finalstate_step, pattern=r'^finalstate_step$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(finalstate_mode, pattern=r'^finalstate_mode$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(add_final_states_mode, pattern=r'^add_final_states_mode$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(delete_final_states_mode, pattern=r'^delete_final_states_mode$'))


    # navigate to transition
    updater.dispatcher.add_handler(CallbackQueryHandler(transition_step, pattern=r'^transition_step$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(transition_mode, pattern=r'^transition_mode$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(add_transition_mode, pattern=r'^add_transition_mode$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(delete_transition_mode, pattern=r'^delete_transition_mode$'))
    

    # navigate to verify finite automata
    updater.dispatcher.add_handler(CallbackQueryHandler(verify_step, pattern=r'^verify_step$'))

    # navigate to test finite automata
    updater.dispatcher.add_handler(CallbackQueryHandler(test_string_step, pattern=r'^test_string_step$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(test_string_handle, pattern=r'^test_string_handle$'))


    # navigate to determinization
    updater.dispatcher.add_handler(CallbackQueryHandler(det_step, pattern=r'^det_step$'))

    # navigate to minimization
    updater.dispatcher.add_handler(CallbackQueryHandler(min_step, pattern=r'^min_step$'))
    
    # navigate to save/load
    updater.dispatcher.add_handler(CallbackQueryHandler(save_step, pattern=r'^save_step$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(save, pattern=r'^save$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(save_new, pattern=r'new_save$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(load, pattern=r'^load$'))

    # and finally the message handler, it handles all messages
    # here the ~Filters.command means that we don't want to handle commands
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
    print("Unloading the context...")
    unload_context(Context.context)
    print("Context unloaded!")
    
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
    if mode == 'delete_state_mode':
        update.message.reply_text(text=delete_state_mode_handle(update, context))
        update.message.reply_text(text=state_mode_msg(update.effective_user.id), reply_markup=state_mode_button())
    if mode == 'add_symbol_mode':
        update.message.reply_text(text=add_symbol_mode_handle(update, context))
        update.message.reply_text(text=symbol_mode_msg(update.effective_user.id), reply_markup=symbol_mode_button())
    if mode == 'delete_symbol_mode':
        update.message.reply_text(text=delete_symbol_mode_handle(update, context))
        update.message.reply_text(text=state_mode_msg(update.effective_user.id), reply_markup=symbol_mode_button())
    if mode == 'add_start_state_mode':
        update.message.reply_text(text=add_start_state_mode_handle(update, context))
        update.message.reply_text(text=startstate_mode_msg(update.effective_user.id), reply_markup=startstate_mode_button())
    if mode == 'delete_start_state_mode':
        update.message.reply_text(text=detete_start_state_mode_handle(update, context))
        update.message.reply_text(text=startstate_mode_msg(update.effective_user.id), reply_markup=symbol_mode_button())
    if mode == 'add_final_states_mode':
        update.message.reply_text(text=add_final_states_mode_handle(update, context))
        update.message.reply_text(text=finalstate_mode_msg(update.effective_user.id), reply_markup=finalstate_mode_button())
    if mode == 'delete_final_states_mode':
        update.message.reply_text(text=delete_final_states_mode_handle(update, context))
        update.message.reply_text(text=finalstate_mode_msg(update.effective_user.id), reply_markup=finalstate_mode_button())
    if mode == 'add_transition_mode':
        update.message.reply_text(text=add_transition_mode_handle(update, context))
    if mode == 'delete_transition_mode':
        update.message.reply_text(text=delete_transition_mode_handle(update, context))

    if mode == 'test_fa':
        update.message.reply_text(text=test_step_handle(update, context))
    if mode == 'load_mode':
        update.message.reply_text(text=load_mode_handle(update, context), reply_markup=just_back())
    
    return

if __name__ == '__main__':
    Context.context = load_context()
    main()