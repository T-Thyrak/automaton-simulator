import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler

def prepare():
    """Prepare the environment."""
    
    # Load environment variables from .env file
    load_dotenv()

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    
    # simply send a message to the user
    update.message.reply_text(f'Hello {update.effective_user.first_name}!')

def main() -> None:
    """Main function."""
    prepare()
    
    
    token = os.getenv('TG_ACCESS_TOKEN') # get the token from the environment variable
    
    # create the updater
    updater = Updater(token=token, use_context=True)
    
    # add the handler for the /start command
    updater.dispatcher.add_handler(CommandHandler('start', start))
    
    # start the bot
    updater.start_polling()
    
    print("Bot has started!")
    
    # do nothing until we stop the bot
    updater.idle()
    
    print("Bot has stopped!")
    
    pass
    
if __name__ == '__main__':
    main()