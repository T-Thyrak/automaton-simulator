from __future__ import annotations

from typing import TypeVar, Callable

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