class State:
    def __init__(self, id: int):
        self.id = id
        
    def __str__(self):
        return f"q{self.id}"
    
    def __repr__(self):
        return f"State(id={self.id})"