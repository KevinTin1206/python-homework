### Assignment basic_oo ###

"""
Assignment: Basic Object-Oriented Programming and Functional Python

This module covers foundational Python concepts including:
- Functional programming tools: `map()`, `filter()`, `lambda` expressions, and list comprehensions.
- Mathematical operations and range processing.
- Object-Oriented Programming (OOP):
  * Class definitions, constructor (`__init__`), and instance methods.
  * Special methods (dunder methods): `__str__` and `__repr__`.
  * Object instantiation and state mutation.
- Data structures and aggregation:
  * Frequency counting with dictionaries.
  * Sorting, filtering, and converting between lists, tuples, and custom objects.
"""

# s1111596_s1099248, Araz Jabrayilov_TIAN

from math import sqrt


# ======================================================================
# Task 1: Temperature Conversion and Mathematical Computations
# ======================================================================

# Task 1a: Convert Fahrenheit to Celsius using map.
def toCelsiusMap(lst):
    """
    Convert a list of temperatures from Fahrenheit to Celsius using `map()`.

    Uses a lambda function implementing the formula: (Fahrenheit - 32) * 5 / 9.

    Args:
        lst (list[float | int]): A list of temperatures in degrees Fahrenheit.

    Returns:
        list[float]: A new list containing the corresponding temperatures in Celsius.
    """
    # map applies the lambda conversion function to each temperature in the list
    return list(map(lambda fahrenheit: (fahrenheit - 32) * 5 / 9, lst))


# Task 1b: Convert Fahrenheit to Celsius using a list comprehension.
def toCelsiusLC(lst):
    """
    Convert a list of temperatures from Fahrenheit to Celsius using a list comprehension.

    Applies the formula (Fahrenheit - 32) * 5 / 9 to each element in a concise,
    Pythonic syntax.

    Args:
        lst (list[float | int]): A list of temperatures in degrees Fahrenheit.

    Returns:
        list[float]: A new list containing the corresponding temperatures in Celsius.
    """
    # Calculate each Celsius value and collect the results in a new list
    return [(fahrenheit - 32) * 5 / 9 for fahrenheit in lst]


# Task 1c: Sum the cubes of even integers, including both bounds.
# Use filter to select the even integers and map to calculate their cubes.
def mathFuncMapFilter(lowerBound, upperBound):
    """
    Calculate the sum of the cubes of all even integers within an inclusive range
    using `filter()` and `map()`.

    Workflow:
    1. Generate the integer range [lowerBound, upperBound] inclusive.
    2. Filter out odd integers, keeping only even numbers (`number % 2 == 0`).
    3. Map each even number to its cube (`number ** 3`).
    4. Compute and return the sum of all cubed values.

    Args:
        lowerBound (int): The lower boundary of the range (inclusive).
        upperBound (int): The upper boundary of the range (inclusive).

    Returns:
        int: The sum of the cubes of all even integers in the range.
    """
    # Generate range including upperBound by adding 1 to the stop parameter
    numbers = range(lowerBound, upperBound + 1)
    # Filter the numbers sequence to retain only even numbers (divisible by 2)
    even_numbers = filter(lambda number: number % 2 == 0, numbers)
    # Compute the cube (power of 3) for each filtered even number
    cubes = map(lambda number: number ** 3, even_numbers)
    # Aggregate and return the total sum of all cubes
    return sum(cubes)


# Task 1d: The same calculation using a list comprehension in one line.
def mathFuncLC(lowerBound, upperBound):
    """
    Calculate the sum of the cubes of all even integers within an inclusive range
    using a single-line list comprehension.

    Combines generation, even parity check, cubing, and summation into a
    single concise expression.

    Args:
        lowerBound (int): The lower boundary of the range (inclusive).
        upperBound (int): The upper boundary of the range (inclusive).

    Returns:
        int: The sum of the cubes of all even integers in the range.
    """
    # Generate range, filter even numbers, cube each number, and sum them all
    return sum([number ** 3 for number in range(lowerBound, upperBound + 1) if number % 2 == 0])


# ======================================================================
# Task 2: Person Class Definition
# ======================================================================

# Task 2: A person with a name, a comment, and an ID.
class Person:
    """
    Represents an individual person with an identifier, name, and comment.

    Attributes:
        name (str): The person's full name.
        comment (str): An optional text comment, initialized to an empty string.
        id (int): The identifier assigned to the person.
    """

    def __init__(self, name, id):
        """
        Initialize a new Person instance.

        Args:
            name (str): The person's name.
            id (int): The identifier for the person.
        """
        self.name = name
        self.comment = ""  # Default comment is initially empty
        self.id = id

    def __str__(self):
        """
        Return a user-friendly string representation of the Person.

        Used by `print()` and `str()`.

        Returns:
            str: Formatted string in the format "Name (id=X)".
        """
        return f"{self.name} (id={self.id})"

    def rename(self, newName):
        """
        Update the person's name with a new value.

        Args:
            newName (str): The updated name for this person.
        """
        self.name = newName


# ======================================================================
# Task 3: Converting a Sequence of Names to Person Objects
# ======================================================================

# Task 3: Create one Person for each name, using its position as its ID.
def toObjectList(names):
    """
    Convert an iterable of name strings into a list of Person objects.

    Each Person's `id` is assigned based on its 0-indexed position in the sequence,
    obtained using Python's built-in `enumerate()`.

    Args:
        names (iterable[str]): A sequence or list of person names.

    Returns:
        list[Person]: A list of newly instantiated Person objects.
    """
    # enumerate() yields pairs of (index, item); index is passed as the person ID
    return [Person(name, index) for index, name in enumerate(names)]


# ======================================================================
# Task 4: Duplicate Name Detection
# ======================================================================

# Task 4: Return each repeated name once, sorted alphabetically, as a tuple.
def getDuplicatesAlphabetical(listOfPersonObjects):
    """
    Find and return all duplicate names among Person objects, sorted alphabetically.

    Workflow:
    1. Count occurrences of each name using a frequency dictionary.
    2. Extract names that occur strictly more than once (`count > 1`).
    3. Sort the duplicate names in alphabetical order (`sorted()`).
    4. Convert the sorted result into an immutable tuple.

    Args:
        listOfPersonObjects (list[Person]): A list of Person instances.

    Returns:
        tuple[str, ...]: An alphabetically sorted tuple of names that appear more than once.
    """
    # Dictionary mapping each name to its frequency count
    counts = {}
    for person in listOfPersonObjects:
        # Increment frequency count for person.name
        counts[person.name] = counts.get(person.name, 0) + 1

    # Filter names that appear more than once
    duplicates = [name for name, count in counts.items() if count > 1]
    # Return as an alphabetically sorted tuple
    return tuple(sorted(duplicates))


# ======================================================================
# Task 5: 2D Point Geometry Class
# ======================================================================

# Task 5: A point in two-dimensional space.
class Point2D:
    """
    Represents a point in a 2-dimensional Cartesian coordinate system.

    Attributes:
        x (float | int): The horizontal coordinate on the X-axis.
        y (float | int): The vertical coordinate on the Y-axis.
    """

    def __init__(self, x, y):
        """
        Initialize a 2D point with X and Y coordinates.

        Args:
            x (float | int): The X-coordinate.
            y (float | int): The Y-coordinate.
        """
        self.x = x
        self.y = y

    def distanceFromOrigin(self):
        """
        Calculate the Euclidean distance from this point to the origin (0, 0).

        Formula: sqrt(x^2 + y^2)

        Returns:
            float: The Euclidean distance from the origin.
        """
        return sqrt(self.x ** 2 + self.y ** 2)

    def halfway(self, target):
        """
        Compute the midpoint between this point and another target Point2D.

        Formula: ((x1 + x2) / 2, (y1 + y2) / 2)

        Args:
            target (Point2D): The other point to calculate the midpoint with.

        Returns:
            Point2D: A new Point2D instance representing the midpoint.
        """
        # Midpoint coordinates are the arithmetic averages of corresponding axes
        return Point2D((self.x + target.x) / 2, (self.y + target.y) / 2)

    def getX(self):
        """
        Get the X-coordinate as a float.

        Returns:
            float: The X-coordinate converted to a floating-point number.
        """
        return float(self.x)

    def getY(self):
        """
        Get the Y-coordinate as a float.

        Returns:
            float: The Y-coordinate converted to a floating-point number.
        """
        return float(self.y)

    # __repr__ returns the object's text representation, also used in lists.
    def __repr__(self):
        """
        Return an unambiguous string representation of the Point2D object.

        This representation is used when inspecting objects or displaying them
        inside collections (e.g., lists).

        Returns:
            str: String formatted as "(x, y)".
        """
        return f"({self.x}, {self.y})"


# ======================================================================
# Example Executions & Demonstration
# ======================================================================
# Examples run only when this file is executed directly.
if __name__ == "__main__":
    # Test Task 1a: Fahrenheit to Celsius conversion using map
    # Expected output: [-40.0, 0.0, 10.0]
    print(toCelsiusMap([-40, 32, 50]))

    # Test Task 1b: Fahrenheit to Celsius conversion using list comprehension
    # Expected output: [-40.0, 0.0, 10.0]
    print(toCelsiusLC([-40, 32, 50]))

    # Test Task 1c: Sum of cubes of even numbers in [10, 100] using map & filter
    # Expected output: 13004200
    print(mathFuncMapFilter(10, 100))

    # Test Task 1d: Sum of cubes of even numbers in [10, 100] using list comprehension
    # Expected output: 13004200
    print(mathFuncLC(10, 100))

    # Test Task 2: Person instantiation, renaming, and string conversion
    person = Person("aName", 4)
    person.rename("aNewName")
    # Expected output: aNewName (id=4)
    print(person)

    # Test Task 3: Converting a list of names into Person objects with sequential IDs
    oL = toObjectList(["Thomas", "Michael", "Thomas"])
    # Expected output:
    # Thomas (id=0)
    # Michael (id=1)
    # Thomas (id=2)
    for person in oL:
        print(person)

    # Test Task 4: Finding duplicate names returned as an alphabetically sorted tuple
    # Expected output: ('Alfred', 'Michael', 'Thomas')
    print(getDuplicatesAlphabetical(toObjectList([
        "Thomas", "Michael", "Thomas", "Susanne",
        "Michael", "Thomas", "Alfred", "Alfred"
    ])))

    # Test Task 5: Point2D operations (distance, midpoint, coordinate access, and repr)
    p = Point2D(3, 4)
    # Distance from origin for (3, 4) -> sqrt(3^2 + 4^2) = 5.0
    print(p.distanceFromOrigin())

    # Midpoint between (3, 4) and (0, 0) -> (1.5, 2.0)
    print(p.halfway(Point2D(0, 0)))

    # Get X coordinate as float and multiply by 100 -> 3.0 * 100 = 300.0
    print(p.getX() * 100)

    # List of Point2D objects displaying via __repr__ -> [(1, 1), (2, 2), (3, 3)]
    print([Point2D(1, 1), Point2D(2, 2), Point2D(3, 3)])
