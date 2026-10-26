### Assignment recap ###

"""
Assignment Recap

This module provides solutions for five core Python programming tasks:
- Task 1: String splitting, list slicing, and filtering with lambda expressions.
- Task 2: Mapping sequence elements to their lengths in a dictionary.
- Task 3: Filtering elements based on capitalization using list comprehensions.
- Task 4: Applying a higher-order function to each item in a list.
- Task 5: Exception handling and safe execution wrapper.
"""

# s1111596_s1099248, Araz Jabrayilov_TIAN


# ----------------------------------------------------------------------
# Task 1: String Processing, List Slicing, and Lambda Filtering
# ----------------------------------------------------------------------
# Use slicing, filter, and a lambda expression.
def process(names, last, notStartingWith):
    """
    Process a comma-separated string of names by slicing up to a specified
    boundary name and filtering out names with a forbidden prefix.

    Workflow:
    1. Split the raw string by commas and strip extraneous whitespace.
    2. Locate the boundary name `last`:
       - If present, slice the list up to and including that name.
       - If absent, retain the entire list.
    3. Filter out any names that start with the prefix `notStartingWith`.

    Args:
        names (str): A comma-separated string containing names.
        last (str): The boundary name marking the end of the slice (inclusive).
        notStartingWith (str): The prefix used to exclude names.

    Returns:
        list[str]: A filtered list of names meeting the criteria.
    """
    # Split the string by commas and remove surrounding whitespace from each name
    name_list = [name.strip() for name in names.split(",")]

    # Determine the slice end index (inclusive of 'last')
    if last in name_list:
        # Slicing upper bound is exclusive, so add 1 to include 'last'
        end = name_list.index(last) + 1
    else:
        # If 'last' is not found, include the entire list
        end = len(name_list)

    # Slice the list from the beginning up to the determined boundary
    selected_names = name_list[:end]

    # Use filter() with a lambda expression to omit names starting with 'notStartingWith'
    return list(filter(
        lambda name: not name.startswith(notStartingWith),
        selected_names
    ))


# ----------------------------------------------------------------------
# Task 2: Map Each Name to Its Character Count
# ----------------------------------------------------------------------
# Map each name to its number of characters.
def toDict(names):
    """
    Map each name in a collection to its character count (length).

    Iterates over the given iterable of names and builds a dictionary
    where each unique name is a key and its length is the corresponding value.

    Args:
        names (iterable of str): A sequence of name strings.

    Returns:
        dict[str, int]: A dictionary mapping each unique name to its length.
    """
    result = {}
    for name in names:
        # Assign the string length as the value for each name key
        result[name] = len(name)
    return result


# ----------------------------------------------------------------------
# Task 3: Filter Strings Starting with a Lowercase Letter
# ----------------------------------------------------------------------
# Use a list comprehension to skip strings starting with a lowercase letter.
def toListSkipLowerCase(tuple):
    """
    Extract strings from a tuple/iterable, skipping those that start with a lowercase letter.

    Evaluates the first character of each string using a list comprehension.
    Strings starting with an uppercase letter, digit, or symbol are kept;
    only strings starting with a lowercase character are omitted.

    Args:
        tuple (tuple of str): An iterable containing string elements.

    Returns:
        list[str]: A list of strings that do not start with a lowercase character.
    """
    # Slicing [:1] avoids IndexError if any string element is empty
    return [name for name in tuple if not name[:1].islower()]


# ----------------------------------------------------------------------
# Task 4: Higher-Order Function - Apply Function to All Elements
# ----------------------------------------------------------------------
# Apply the given function to every item and return the results as a list.
def applyFuncToAll(func, lst):
    """
    Apply a callable function to each item in a list and return the results.

    Implements higher-order mapping logic by invoking `func(item)` for every
    element and collecting the transformed outputs in a new list.

    Args:
        func (callable): A function that accepts an item and returns a transformed value.
        lst (list): A list of items to process.

    Returns:
        list: A new list containing the return values of `func(item)` for each element in `lst`.
    """
    result = []
    for item in lst:
        # Call the passed function on the current item and append the result
        result.append(func(item))
    return result


# ----------------------------------------------------------------------
# Task 5: Safe Function Invocation and Exception Handling
# ----------------------------------------------------------------------
# Return the function result or the required message if an exception occurs.
def swallowException(func):
    """
    Safely execute a zero-argument callable and handle potential exceptions.

    Execution logic:
    - If `func()` succeeds, its return value is returned directly.
    - If a `ZeroDivisionError` is raised, returns a custom division-by-zero error message.
    - If any other `Exception` is raised, returns a generic fallback error message.

    Args:
        func (callable): A zero-argument function/lambda to execute.

    Returns:
        Any: The result of `func()` or a descriptive string if an exception was caught.
    """
    try:
        # Attempt to invoke the callable
        return func()
    except ZeroDivisionError:
        # Handle division-by-zero specifically
        return "only chuck norris is allowed to divide by zero"
    except Exception:
        # Handle all other general exceptions (IndexError, TypeError, ValueError, etc.)
        return "something went wrong"


if __name__ == "__main__":
    # ------------------------------------------------------------------
    # Test Cases for Task 1
    # ------------------------------------------------------------------
    # Test 1: Slices up to 'Fabian' and filters out names starting with 'A' ('Andrea')
    assert process(
        "Thomas, Michael, Thomas, Andrea, Barbara, Susanne, Michael, Fabian, Hans",
        "Fabian",
        "A"
    ) == [
        "Thomas", "Michael", "Thomas", "Barbara", "Susanne", "Michael", "Fabian"
    ]
    # Test 2: 'NotInList' is not in list -> processes all names, excluding those starting with 'Bar'
    assert process("Andrea, Barbara", "NotInList", "Bar") == ["Andrea"]

    # ------------------------------------------------------------------
    # Test Cases for Task 2
    # ------------------------------------------------------------------
    # Compare both the keys and values of the dictionary.
    assert toDict([
        "Thomas", "Michael", "Thomas", "Barbara", "Susanne", "Michael", "Fabian"
    ]) == {
        "Barbara": 7,
        "Fabian": 6,
        "Michael": 7,
        "Susanne": 7,
        "Thomas": 6
    }

    # ------------------------------------------------------------------
    # Test Cases for Task 3
    # ------------------------------------------------------------------
    # Exclude strings starting with lowercase letters ('hans', 'max', 'toni')
    assert toListSkipLowerCase(
        ("hans", "Fritz", "max", "Petra", "Susanne", "toni")
    ) == ["Fritz", "Petra", "Susanne"]
    # All strings start with lowercase letters -> expected empty list
    assert toListSkipLowerCase(("hans", "max")) == []

    # ------------------------------------------------------------------
    # Test Cases for Task 4
    # ------------------------------------------------------------------
    # Double each integer
    assert applyFuncToAll(lambda i: i * 2, [1, 2, 3]) == [2, 4, 6]
    # Compute the length of each string
    assert applyFuncToAll(len, ["a", "bb", "ccc"]) == [1, 2, 3]

    # ------------------------------------------------------------------
    # Test Cases for Task 5
    # ------------------------------------------------------------------
    # Normal execution without exceptions
    assert swallowException(lambda: 100) == 100
    # ZeroDivisionError caught -> returns custom Chuck Norris message
    assert swallowException(lambda: 100 / 0) == (
        "only chuck norris is allowed to divide by zero"
    )
    # IndexError caught -> returns generic error message
    assert swallowException(lambda: [1, 2, 3][5]) == "something went wrong"

    print("All 10 example tests passed.")
