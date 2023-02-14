import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler

def prepare():
    """Prepare the environment."""
    load_dotenv()

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Hello {update.effective_user.first_name}!')

def main() -> None:
    """Main function."""
    prepare()
    
    token = os.getenv('TG_ACCESS_TOKEN')
    updater = Updater(token=token, use_context=True)
    
    updater.dispatcher.add_handler(CommandHandler('start', start))
    
    updater.start_polling()
    
    print("Bot has started!")
    updater.idle()
    
    print("Bot has stopped!")
    
    pass

if __name__ == '__main__':
    main()