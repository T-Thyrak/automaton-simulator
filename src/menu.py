from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from fa import FA

from context import Context

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
            InlineKeyboardButton("Save/Load FA", callback_data='save_step'),
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

# Menu handler when called from a callback query
def call_menu(update: Update, context: CallbackContext) -> None:
    """Calls the menu."""
    
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(text=menu_message(), reply_markup=menumode_keyboard())