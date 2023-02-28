import re

def validate_symbol(sym: str) -> bool:
    """Validate that symbol is valid."""
    
    if sym == 'eps':
        return True
    else:
        pattern = r'^.$'
        return re.match(pattern, sym) is not None


i = input('enter sym : ')

print(validate_symbol(i))

# from sym import Symbol

# print(repr(Symbol('a')))
