from fa import FA
from dill import load, dump

context: dict[str, FA] = {}

def unload_context():
    with open('misc/context.dill', 'wb') as file:
        dump(context, file)
        
def load_context():
    try:
        with open('misc/context.dill', 'rb') as file:
            context = load(file)
    except EOFError:
        context = {}