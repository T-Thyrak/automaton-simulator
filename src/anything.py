from typing import TypeVar, Callable

T = TypeVar('T')
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