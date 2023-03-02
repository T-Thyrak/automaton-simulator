import os
from dotenv import load_dotenv
from telegram import *
from telegram.ext import *

load_dotenv()

# 5-tuple collection
states = []
symbols = []
start_state = ""
final_states = []
transitions = {}
input_string = ''

def start_command(update: Update, context: CallbackContext):
    update.message.reply_text('Welocme To Testing Finite Automata Bot!')
    update.message.reply_text('Enter the input string to run the automaton: ')

def get_states(update: Update, context: CallbackContext):
    states = update.message.text
    states = states.split()
    print(states)
    update.message.reply_text(get_symbols(update, context))

def get_symbols(update: Update, context: CallbackContext):
    update.message.reply_text('Enter the automaton alphabets separated by space: ')
    symbols = update.message.text
    symbols = symbols.split()
    print(symbols)
    update.message.reply_text(get_start_state(update, context))

def get_start_state(update: Update, context: CallbackContext):
    update.message.reply_text('Enter the start state of the automaton: ')
    start_state = update.message.text
    print(start_state)
    update.message.reply_text(get_final_state(update, context))

def get_final_state(update: Update, context: CallbackContext):
    update.message.reply_text('Enter the final state of the automaton: ')
    final_states = update.message.text
    final_states = final_states.split()
    print(final_states)
    update.message.reply_text(get_transitions(update, context))

def get_transitions(update: Update, context: CallbackContext):
    update.message.reply_text('Enter the next states for the following (enter . for dead/reject state)')
    for state in states:
        for sym in symbols:
            print(f"\t  {sym}")
            print(f"{state}\t---->\t", end="")
            update.message.reply_text(f"{state}\t---->\t with {sym} get: ")
            dest = update.message.text
            
            # Rejected states are represented as None in the dictionary
            if dest == ".":
                transitions[(state, sym)] = None
            else:
                transitions[(state, sym)] = dest
    
    print(transitions)
    update.message.reply_text(test_string(update, context))

def test_string(update: Update, context: CallbackContext):
    update.message.reply_text("Enter the input string to run the automaton: ")
    input_string = update.message.text

    # Start parsing the input string with the current state as start state
    current_state = start_state

    for char in input_string:
        # Transition to the next state using the current state and input alphabet
        current_state = transitions[(current_state, char)]
        
        # Check whether the DFA goes into a dead/rejected state
        if current_state is None:
            print("Rejected")
            update.message.reply_text('Rejected')
            break
        else:
            # When entire string is parsed, check whether the final state is an accepted state
            if (current_state in final_states):
                print("Accepted")
                update.message.reply_text('Accepted')
            else:
                print("Rejected")
                update.message.reply_text('Rejected')

def error(update: Update, context: CallbackContext):
    print(f'Update {update} caused error: {context.error}')

def main() -> None:
    updater = Updater(token=os.getenv('TG_ACCESS_TOKEN'), use_context=True)
    dp = updater.dispatcher

    #Command
    dp.add_handler(CommandHandler('start', start_command))

    #Messge
    dp.add_handler(MessageHandler(Filters.text, get_states))

    #Error
    dp.add_error_handler(error)

    #Run the bot
    updater.start_polling()

    print('Starting up bot.....')

    updater.idle()

if __name__ == '__main__':
    main()








