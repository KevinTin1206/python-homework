

# Newton's Method: Approximating Square Roots
#s1111596_s1099248, Araz Jabrayilov_TIAN
# Original source description from the supplied file:
# This is a Python port of the LISP implementation described in
# "Structure and Interpretation of Computer Programs" by Abelson/Sussman,
# book page 28: https://web.mit.edu/6.001/6.037/sicp.pdf
#
# PROGRAM OBJECTIVE
# Find an approximate square root of a positive number x.
# A square root is a number whose square equals x.
# For example, the positive square root of 9 is 3 because 3 * 3 = 9.
#
# MAIN IDEA
# 1. Start with a guess of 1.0.
# 2. Check whether the square of the guess is close enough to x.
# 3. If not, improve the guess using: (guess + x / guess) / 2.
# 4. Repeat until the stopping condition is satisfied.
#
# This annotated version preserves all six original functions and their logic.
# The examples at the bottom remain commented out, as in the supplied file.
# No imports or additional libraries are required.


# ---------------------------------------------------------------------------
# 1. Calculate the square of a number.
# ---------------------------------------------------------------------------
def square(x):
    # x is the argument received by this particular function call.
    # Multiplying a number by itself gives its square: square(3) returns 9.
    # return sends the result back to the caller; it does not print anything.
    return x * x


# ---------------------------------------------------------------------------
# 2. Calculate the arithmetic mean of two numbers.
# ---------------------------------------------------------------------------
def average(x, y):
    # Add the two arguments and divide their sum by 2.
    # Parentheses make the addition happen before the division.
    # For example, average(1.0, 9.0) returns 5.0.
    # In Python 3, / performs division and produces a floating-point result
    # for these ordinary integer or floating-point inputs.
    return (x + y) / 2


# ---------------------------------------------------------------------------
# 3. Decide whether the current guess is accurate enough.
# ---------------------------------------------------------------------------
def isGoodEnough(guess, x):
    # guess is the current approximation; x is the original target number.
    # square(guess) calls the helper function defined above.
    # Subtracting x measures how far the squared guess is from the target.
    # abs() removes the sign, so errors on either side are treated equally.
    # The comparison returns a Boolean value: either True or False.
    #
    # Example: for guess = 3.0001 and x = 9,
    # abs(3.0001 * 3.0001 - 9) is about 0.00060001, so this returns True.
    #
    # IMPORTANT: 0.001 is a tolerance for the SQUARED guess, not for the
    # difference between guess and the exact square root. It does not mean
    # that every returned square root is correct to three decimal places.
    return abs(square(guess) - x) < 0.001


# ---------------------------------------------------------------------------
# 4. Produce a better approximation using Newton's update formula.
# ---------------------------------------------------------------------------
def improve(guess, x):
    # When guess is positive and too small, x / guess is above the root.
    # When guess is positive and too large, x / guess is below the root.
    # Taking their average produces the next guess.
    #
    # Python first evaluates x / guess and then calls average().
    # Example: improve(1.0, 9) calls average(1.0, 9.0), returning 5.0.
    # The next improvement is average(5.0, 9 / 5.0), which returns 3.4.
    #
    # guess must not be zero because x / guess would divide by zero.
    # For ordinary positive inputs, starting at 1.0 keeps guesses positive.
    return average(guess, x / guess)


# ---------------------------------------------------------------------------
# 5. Repeat the approximation process using recursion.
# ---------------------------------------------------------------------------
def sqrtIter(guess, x):
    # Recursion means that a function calls itself.
    # Each call receives the current guess and the unchanged target x.
    if isGoodEnough(guess, x):
        # BASE CASE: the stopping condition is satisfied.
        # Return the approximation without making another recursive call.
        return guess
    else:
        # RECURSIVE CASE: the current approximation is not accurate enough.
        # First, improve(guess, x) calculates a new guess.
        # Then, sqrtIter(new_guess, x) checks that new guess in another call.
        # The target x stays the same; only the guess changes.
        #
        # The outer return is essential: it passes the result of the deeper
        # call back through the earlier calls to the original caller.
        # Without it, this branch would return None after the inner call ends.
        return sqrtIter(improve(guess, x), x)


# ---------------------------------------------------------------------------
# 6. Provide a simple starting function for the user.
# ---------------------------------------------------------------------------
def newton(x):
    # The caller only supplies the number whose square root is needed.
    # This function chooses 1.0 as the initial guess and starts the recursion.
    # It returns the approximation produced by sqrtIter().
    return sqrtIter(1.0, x)


# EXAMPLE CALL SEQUENCE FOR newton(9)
# newton(9)
#   -> sqrtIter(1.0, 9)
#   -> sqrtIter(5.0, 9)
#   -> sqrtIter(3.4, 9)
#   -> sqrtIter(3.023529411764706, 9)
#   -> sqrtIter(3.00009155413138, 9)
# At the last step, the squared error is less than 0.001.
# That guess is returned through the recursive calls and finally to the user.
# These steps describe separate function calls, not a list built by the code.
#
# LIMITATIONS OF THE ORIGINAL TEACHING EXAMPLE
# The intended inputs are ordinary positive numbers.
# Negative inputs are not validated and are outside this real-root example.
# The fixed squared-error tolerance gives poor relative accuracy near zero.
# For x = 0, for example, the returned approximation is 0.03125, not exactly 0.
# Very large inputs can encounter floating-point or recursion limitations.
# These limitations are documented here without changing the original method.
#
# OPTIONAL DEMONSTRATION
# Remove the leading # from each of the following three lines to enable it.
# __name__ == "__main__" is True when this file is run directly.
# If another file imports this module, the guarded examples will not run.
# print() displays the returned approximation in the terminal.
#
# if __name__ == "__main__":
#     print(newton(4))  # Approximately 2.0000000929222947.
#     print(newton(9))  # Approximately 3.00009155413138.
