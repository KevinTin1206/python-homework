### Assignment hop_decorator ###

# Student information: replace the placeholders below before submission.
# s1111596_s1099248, Araz Jabrayilov_TIAN
# If this is an individual submission, enter only your own information.

# This assignment practices inner functions, scope, higher-order functions,
# decorators, argument forwarding, execution timing, and memoization.
# All implementation comments and explanations are in English.

import time
from functools import wraps


# ===========================================================================
# Task 1: Newton's Method using inner functions
# ===========================================================================
# Keep square() and average() as separate functions, as required.
# Move isGoodEnough(), improve(), and sqrtIter() inside newton().
# These inner functions can read x from the enclosing newton() call, so x
# no longer needs to be passed as an argument to each helper function.


def square(x):
    """Return the square of x."""
    # For example, square(3) returns 3 * 3, which is 9.
    return x * x


def average(x, y):
    """Return the arithmetic mean of x and y."""
    # Parentheses ensure that addition happens before division.
    return (x + y) / 2


def newton(x):
    """Approximate a square root using the original recursive algorithm."""
    # Each call to newton() has its own local x.
    # The inner functions below can access that x through the enclosing scope.
    # This is why their parameter lists contain only guess.
    # No global variable or global declaration is needed.

    def isGoodEnough(guess):
        # Compare the squared approximation with the original target x.
        # abs() makes the difference non-negative; < returns True or False.
        # Keep the original tolerance: the absolute difference between the
        # squared guess and x must be below 0.001.
        # This is not a guarantee of three correct decimal places in the root.
        return abs(square(guess) - x) < 0.001

    def improve(guess):
        # Newton's update for a square root is (guess + x / guess) / 2.
        # Retain the average() helper instead of simplifying the expression.
        # For x = 9 and guess = 1.0, the next guess is (1.0 + 9.0) / 2 = 5.0.
        return average(guess, x / guess)

    def sqrtIter(guess):
        # Base case: stop making recursive calls once the guess is good enough.
        if isGoodEnough(guess):
            return guess
        else:
            # First calculate an improved guess, then check it in another call.
            # x stays available from newton(); it is not passed repeatedly.
            # return passes the final answer back through the earlier calls.
            return sqrtIter(improve(guess))

    # Defining the inner functions above does not run their bodies.
    # This call starts the actual calculation with an initial guess of 1.0.
    return sqrtIter(1.0)


# ===========================================================================
# Task 2: Newton's Method Simplified and Pythonified
# ===========================================================================
# Use a while loop to express repeated improvement directly.
# Keep the same starting guess, update formula, and stopping tolerance.
# Do not replace the algorithm with math.sqrt(x) or x ** 0.5.


def newtonPy(x):
    """Approximate a square root using a loop instead of recursive calls."""
    guess = 1.0

    # Keep improving while the squared guess differs too much from x.
    # >= is the opposite of the original successful condition < 0.001.
    while abs(guess * guess - x) >= 0.001:
        # The right-hand side uses the current guess.
        # Assignment then replaces guess with the improved value.
        guess = (guess + x / guess) / 2

    # Reaching this line means the loop's condition has become False.
    return guess


# Both Newton functions follow the original teaching example's numeric scope:
# use ordinary positive numbers. Negative numbers are not supported here.
# This fixed tolerance on the squared guess gives poor relative accuracy near zero;
# for example, both functions return 0.03125 for x = 0 rather than exactly 0.
# Extreme inputs can encounter floating-point limits; the recursive version
# also has Python's recursion limit. A general-purpose numeric library would
# need a more robust stopping rule and input validation.


# ===========================================================================
# Task 3: log Decorator
# ===========================================================================
# A decorator receives a function and returns another function.
# The returned wrapper adds behavior around a call to the original function.
#
# Writing:
#     @log
#     def helperfunction(a, b): ...
# is equivalent to defining helperfunction first and then assigning:
#     helperfunction = log(helperfunction)
#
# log(func) runs when decoration happens. Its wrapper runs later, each time
# the decorated function is called. These are two different moments.


def log(func):
    """Log a successful call's name, positional arguments, and result."""

    # wraps() preserves metadata such as the original function's name and
    # docstring. It does not execute func or change its returned result.
    @wraps(func)
    def wrapper(*args):
        # In a parameter list, *args collects positional arguments into a tuple.
        # Calling helperfunction(1, 2) therefore gives args == (1, 2).
        # An argument-free call gives the empty tuple ().
        # In a call, *args does the reverse: it unpacks the tuple so func
        # receives the original separate arguments, not one tuple argument.
        result = func(*args)

        # repr() creates a readable representation of each argument.
        # For integers 1 and 2, argument_texts becomes ["1", "2"].
        # Strings keep their quotes, making their type clearer in the log.
        argument_texts = [repr(arg) for arg in args]

        # join() combines the pieces with commas and no additional spaces.
        # This matches the required example: helperfunction(1,2).
        arguments = ",".join(argument_texts)
        print(f"@log: {func.__name__}({arguments}) -> {result}")

        # Printing is not the same as returning. The caller must still receive
        # the original result, so never omit this return statement.
        return result

    # Return the wrapper FUNCTION without parentheses.
    # Returning wrapper() would call it now instead of saving it for later.
    return wrapper


# ===========================================================================
# Task 4: timeMe Decorator
# ===========================================================================
# Measure elapsed time using time.time(), as explicitly required.
# Support any number of positional arguments; keyword arguments are outside
# this exercise's required interface, so no **kwargs parameter is included.


def timeMe(func):
    """Print the duration of a successful call and preserve its result."""

    @wraps(func)
    def wrapper(*args):
        # time.time() returns a wall-clock timestamp measured in seconds.
        # Record it immediately before executing the original function.
        start = time.time()

        # Run the original function exactly once and keep its return value.
        # *args forwards zero, one, or many positional arguments.
        result = func(*args)

        # Record the timestamp immediately after the function finishes.
        # Subtract timestamps to obtain elapsed seconds, then convert to ms.
        elapsed_milliseconds = (time.time() - start) * 1000

        # :.2f displays two digits after the decimal point.
        # Actual durations vary between runs and between computers.
        print(f"@timeMe: {elapsed_milliseconds:.2f} milliseconds")

        # Preserve the original return value, including None or 0.
        return result

    return wrapper


# ===========================================================================
# Task 5: memoization Decorator
# ===========================================================================
# Memoization means remembering earlier results instead of recomputing them.
# A cache maps a set of input arguments to the result of that function call.
# This is appropriate for functions such as fib whose result depends on the
# inputs and whose repeated execution has no required external side effects.


def memo(func):
    """Cache results for hashable positional arguments."""
    # Create the dictionary ONCE for this decorated function.
    # Every later call to wrapper() shares this dictionary through a closure.
    # A different function decorated with @memo gets a separate dictionary.
    # Putting cache = {} inside wrapper() would reset it on every call.
    cache = {}

    @wraps(func)
    def wrapper(*args):
        # Use the whole argument tuple as the dictionary key.
        # fib(5) uses (5,), while a two-argument call might use (2, 3).
        # The comma in (5,) marks a one-element tuple.
        # Dictionary keys must be hashable: integers work, but lists do not.
        # This exercise uses positional arguments, without keyword arguments.
        if args not in cache:
            # Cache miss: compute the result once and save it.
            cache[args] = func(*args)

        # Cache hit: return the saved result without running func again.
        # Test key membership, not the truth value of the saved result:
        # 0, False, and None are also valid results that should be cached.
        return cache[args]

    return wrapper


@memo
def fib(n):
    """Return the n-th Fibonacci number for a non-negative integer n."""
    # Base cases: fib(0) = 0 and fib(1) = 1.
    if n < 2:
        return n
    else:
        # Each later number is the sum of its two predecessors.
        # After decoration, the name fib refers to memo's wrapper.
        # Therefore these recursive calls also check the cache.
        return fib(n - 1) + fib(n - 2)


# WHY IS fib(35) SLOW WITHOUT MEMOIZATION?
# Consider fib(5): it requests fib(4) and fib(3).
# fib(4) also requests fib(3), so the same subproblem is repeated.
# This duplication continues throughout the recursion tree, causing an
# exponentially growing number of calls without caching.
# With @memo, each distinct n is computed once and its result is reused.
# For fib(35) with a fresh cache, only the 36 distinct inputs 0 through 35
# need their results calculated. Later fib(35) calls reuse the saved result.
# Memoization reduces repeated work but still uses memory and recursion.


# ===========================================================================
# Demonstrations: run this file directly to execute the examples.
# ===========================================================================
# This guard prevents printing and sleeping when another file imports the
# functions. The timing examples below deliberately sleep for 1 + 6 seconds,
# so a complete direct run takes approximately seven seconds.

if __name__ == "__main__":
    print("Task 1: Newton's method with inner functions")
    print(newton(4))
    print(newton(9))

    print("\nTask 2: Newton's method with a while loop")
    print(newtonPy(4))
    print(newtonPy(9))

    print("\nTask 3: Logging a function call")

    @log
    def helperfunction(a, b):
        return a + b

    # Prints exactly: @log: helperfunction(1,2) -> 3
    # Assigning its result also demonstrates that the decorator returns 3.
    helper_result = helperfunction(1, 2)
    print(f"Returned value: {helper_result}")

    print("\nTask 4: Timing functions with different numbers of arguments")

    @timeMe
    def testFunctionTime():
        # Avoid naming the variable sum, which would hide Python's sum().
        total = 0
        for i in range(10000):
            total += i
        # No explicit return means the function returns None.

    @timeMe
    def testFunctionTime2(t):
        time.sleep(t)

    @timeMe
    def testFunctionTime3(*args):
        total = 0
        for a in args:
            total += a
        time.sleep(total)

    testFunctionTime()
    testFunctionTime2(1)
    testFunctionTime3(1, 2, 3)

    print("\nTask 5: Memoized Fibonacci numbers")
    print(f"fib(5) = {fib(5)}")       # 5
    print(f"fib(35) = {fib(35)}")     # 9227465
    # map() applies fib to each integer from 0 to 19.
    # list() collects the results so they can be displayed together.
    print(list(map(fib, range(20))))
