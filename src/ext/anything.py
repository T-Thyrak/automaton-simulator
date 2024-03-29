from __future__ import annotations

from typing import TypeVar, Callable, Iterable
import random

T = TypeVar('T')
U = TypeVar('U')

def intersection(lst1: list[T], lst2: list[T], key: Callable[[T, T], bool] = None) -> list[T]:
    if key:
        ints = []
        for i in lst1:
            for j in lst2:
                if key(i, j):
                    ints.append(i)
                    
        return ints
    else:
        return [i for i in lst1 if i in lst2]
    
def union(lst1: list[T], lst2: list[T], key: Callable[[T, T], bool] = None) -> list[T]:
    if key:
        new_lst = lst1.copy()
        for i in lst2:
            if not any(key(i, j) for j in lst1):
                new_lst.append(i)
        
        return new_lst
    else:
        return list(set(lst1 + lst2))

def difference(lst1: list[T], lst2: list[T], key: Callable[[T, T], bool] = None) -> list[T]:
    if key:
        new_lst = []
        for i in lst1:
            if not any(key(i, j) for j in lst2):
                new_lst.append(i)
        
        return new_lst
    else:
        return [i for i in lst1 if i not in lst2]
    
def dequote(s: str) -> str:
    if s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    elif s[0] == '\'' and s[-1] == '\'':
        return s[1:-1]
    else:
        return s
    
def table_drop(dict: dict[tuple[int, int], bool], *, key: Callable[[int, int], bool]) -> dict[tuple[int, int], bool]:
    new_dict = {}
    for k, v in dict.items():
        if not key(*k):
            new_dict[k] = v
            
    return new_dict 

def position_of(ordered_iterable: list[T], *, key: Callable[[T], bool]) -> int | None:
    for i, v in enumerate(ordered_iterable):
        if key(v):
            return i
        
    return None

def choose(iterable: Iterable[T]) -> T:
    return random.choice(list(iterable))

def prune_none(d: dict[T, U]) -> dict[T, U]:
    return {k: v for k, v in d.items() if v is not None}