# The `Result` Class

## Table of Contents

- [The `Result` Class](#the-result-class)
  - [Table of Contents](#table-of-contents)
  - [Background](#background)
    - [Category Theory and Monads](#category-theory-and-monads)
  - [`Result` class (also known as `Either`)](#result-class-also-known-as-either)
  - [Okay, whatever you've got is cool, but what use is it?](#okay-whatever-youve-got-is-cool-but-what-use-is-it)

## Background

### Category Theory and Monads

If I had to explain to you what category theory is and what monads truly are,
I'll end up writing a 200 page book, so I'll give you the shortest possible
explanation.

Category theory is a branch of mathematics that studies the properties of
functions. It's a very abstract branch of mathematics.

Monads are a way to compose functions in category theory. They are a way to
compose functions that return a value wrapped in a context. Specifically, they
define three things:

- A type constructor `m` that takes one type argument and wraps a value of that
  type in a context.
- A function `return` that takes a value and wraps it in a context.
- A function `>>=` (called `bind`) that takes a `m a` value, a function `a -> m b`
    and returns a `m b` value.

and they obey three laws:

- **Left Identity**: `return a >>= f ≡ f a`
- **Right Identity**: `m >>= return ≡ m`
- **Associativity**: `(m >>= f) >>= g ≡ m >>= (\x -> f x >>= g)`

## `Result` class (also known as `Either`)

The `Result` class is a monad that represents a value that may or may not be
present. It's also known as the `Either` monad.

It has two constructors:

- `Ok` - represents a value that is present (`Left` in Haskell)
- `Err` - represents a value that is not present (`Right` in Haskell)

And there we go, our `return` function.

The `>>=` function is a bit more complicated. It takes a `Result a` value, a
function `a -> Result b` and returns a `Result b` value.

```hs
(>>=) :: Result a -> (a -> Result b) -> Result b
(>>=) x f = case x of
    Ok a -> f a
    Err e -> Err e
```

The `>>=` will try to compute the value of `f a` if `x` is `Ok a`. If `x` is
already `Err e`, it will return `Err e` without trying to compute `f a`.

## Okay, whatever you've got is cool, but what use is it?

The `Result` class is useful when you want to mark a function that may fail.

For example, consider the following function:

```py
def divide(a, b) -> float:
    return a / b
```

This function will fail if `b` is `0`. We can mark this function as a function
that may fail by using the `Result` class:

```py
def divide(a, b) -> Result[float, str]:
    if b == 0:
        return Result.Err("Division by zero")
    else:
        return Result.Ok(a / b)
```

Now, we can handle the error without having to deal with exceptions.

```py
result = divide(1, 0)
if result.is_ok():
    print(f"Division result: {result.unwrap()}")
else:
    print(f"Error: {result.unwrap_err()}")
```

Now let's consider another function:

```py
def sqrt(a) -> float:
    return a ** 0.5
```

This function will fail if `a` is negative. We can also mark this function as a
function that may fail by using the `Result` class:

```py
def sqrt(a) -> Result[float, str]:
    if a < 0:
        return Result.Err("Square root of negative number")
    else:
        return Result.Ok(a ** 0.5)
```

So let's say we want to compute the square root of the result of the division
function.

Without the `Result` class, we would have to do something like this:

```py
try:
    result = divide(1, 0)
except DivisionByZeroException:
    print(f"Error: Division by zero")
    return

if result < 0:
    print(f"Error: Square root of negative number")
    return
else:
    root_result = sqrt(result)

print(f"Square root of division result: {root_result}")
```

Just ugly.

With the `Result` class, we can do this:

```py
result = divide(1, 0)
if result.is_err():
    print(f"Error: {result.unwrap_err()}")
    return

root_result = sqrt(result.unwrap())
if root_result.is_err():
    print(f"Error: {root_result.unwrap_err()}")
    return

print(f"Square root of division result: {root_result.unwrap()}")
```

and with the `>>=` operator (in `Result`, I named it `map`), we can do this:

```py
sqrt_result = divide(1, 0).bind(sqrt)
if sqrt_result.is_err():
    print(f"Error: {sqrt_result.unwrap_err()}")
    return

print(f"Square root of division result: {sqrt_result.unwrap()}")
```

And that's it. You can chain as many functions as you want, and if any of them
fails, the chain will stop and the error will be returned.

That's the power of the `Result` class.
