class State:
    def __init__(self, id: int):
        self.id = id
        
    def __str__(self):
        return f"q{self.id}"
    
    def __repr__(self):
        return f"State(id={self.id})"
    
    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)