import re

def validate_state_name(name: str) -> bool:
    """Validate that state name is valid."""
    
    pattern = r'^q(\d+)$'
    return re.match(pattern, name) is not None