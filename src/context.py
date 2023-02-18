from dill import load, dump
import os

class Context:
    context = {}

def unload_context(context: dict[int, dict]):
    if not os.path.exists('misc'):
        os.mkdir('misc')
    
    with open('misc/context.dill', 'wb') as file:
        dump(context, file)
        
def load_context() -> dict[int, dict]:
    try:
        with open('misc/context.dill', 'rb') as file:
            context = load(file)
    except EOFError:
        context = {}
    except FileNotFoundError:
        context = {}
        
    return context