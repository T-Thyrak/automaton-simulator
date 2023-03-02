import os
from dotenv import load_dotenv
from telegram import *
from telegram.ext import *

load_dotenv()

print('Starting up bot.....')

def start_command(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! I\'m a bot. Nice to meet you')

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Try typing anything and I will response')

def custom_command(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! I\'m a custom command. Nice to meet you')

def handle_response(text: str) -> str:
    if 'hello' in text:
        return 'Hey there!'

    if 'how are you' in text:
        return 'I am good, Thanks!'

    return 'IDK'

def handle_message(update: Update, context):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = ''

    print(f'User ({update.message.chat_id}) says: "{text} in: {message_type}"')

    if message_type == 'group':
        if '@neathautobot' in text:
            new_text = text.replace('@neathautobot', '').strip()
            response = handle_response(new_text)
    else:
        response = handle_response(text)
    
    update.message.reply_text(response)

def error(update: Update, context: CallbackContext):
    print(f'Update {update} caused error: {context.error}')


if __name__ == '__main__':
    updater = Updater(token=os.getenv('TG_ACCESS_TOKEN'), use_context=True)
    dp = updater.dispatcher

    #Command
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('custom', custom_command))

    #Messge
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    #Error
    dp.add_error_handler(error)

    #Run the bot
    updater.start_polling(1.0)
    updater.idle()

