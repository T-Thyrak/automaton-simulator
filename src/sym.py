class Symbol:
    def __init__(self, symbol: str):
        self.symbol = symbol
        
    def __str__(self):
        return self.symbol
    
    def __repr__(self):
        return f"Symbol(symbol={self.symbol})"
    
    def __eq__(self, other):
        return self.symbol == other.symbol
    
    def __ne__(self, other):
        return self.symbol != other.symbol
    
    def __hash__(self):
        return hash(self.symbol)