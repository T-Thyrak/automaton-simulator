from __future__ import annotations

from enum import Enum
from typing import TypeVar, Callable, Generic

T = TypeVar('T')
U = TypeVar('U')
R = TypeVar('R')

class UnwrapException(Exception):
    pass

class ResultVariant(Enum):
    OK = 0
    ERROR = 1

class Result(Generic[T, U]):
    def __init__(self, variant: ResultVariant, value: T = None, error: U = None):
        self.variant = variant
        self.value = value
        self.error = error
        
    def __repr__(self):
        return f"Result({self.variant}, {self.value}, {self.error})"
    
    @staticmethod
    def Ok(value: T) -> Result[T, U]:
        return Result(ResultVariant.OK, value)

    @staticmethod
    def Err(error: U) -> Result[T, U]:
        return Result(ResultVariant.ERROR, error=error)
    
    def unwrap(self) -> T:
        if self.variant == ResultVariant.OK:
            return self.value
        else:
            raise UnwrapException("Cannot unwrap error result")
    
    def unwrap_err(self) -> U:
        if self.variant == ResultVariant.ERROR:
            return self.error
        else:
            raise UnwrapException("Cannot unwrap ok result")
        
    def is_ok(self) -> bool:
        return self.variant == ResultVariant.OK
    
    def is_err(self) -> bool:
        return self.variant == ResultVariant.ERROR
    
    def map(self, f: Callable[[T], R]) -> Result[R, U]:
        if self.variant == ResultVariant.OK:
            return Result.Ok(f(self.value))
        else:
            return Result.Err(self.error)
        
    def map_err(self, f: Callable[[U], R]) -> Result[T, R]:
        if self.variant == ResultVariant.ERROR:
            return Result.Err(f(self.error))
        else:
            return Result.Ok(self.value)