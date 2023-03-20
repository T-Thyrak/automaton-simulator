import re

def validate_state_name(name: str) -> bool:
    """Validate that state name is valid."""
    
    pattern = r'^q(\d+)$'
    return re.match(pattern, name) is not None

def validate_symbol(sym: str) -> bool:
    """Validate that symbol is valid."""
    
    
    pattern = r'^.$'
    return re.match(pattern, sym) is not None

# from sym import Symbol

# print(repr(Symbol('a')))
