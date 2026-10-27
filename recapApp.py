### Assignment recapApp ###

# TODO: Fill in your actual student ID and surname before submission; if this is an individual assignment, only fill in your own information.
# s1111596_s1099248, Araz Jabrayilov_TIAN

# Program objective: Read student grades, filter passing students, curve grades, display statistics, and save the results.
# The structure of students is always a list where each tuple represents a student:
# [(student_id, name, grade), ...]
# For example: [("12345", "Alice", 89), ("12346", "Bob", 74)]

import csv
from pathlib import Path


# ================================
# Task 1: File Reading
# ================================

def read_grades(filename):
    """Reads a CSV file and returns a list of student tuples; displays an error and returns an empty list if the file is not found."""
    students = []

    try:
        # `with` automatically closes the file when done, even if an exception occurs.
        # "r" stands for read; encoding="utf-8" specifies text encoding.
        # When reading/writing with csv module, newline="" lets it handle newlines properly.
        with open(filename, "r", encoding="utf-8", newline="") as file:
            # The data is semicolon-separated, e.g.: 12345;Alice;89.
            # There is no header row, so the first row is also student data and must not be skipped.
            reader = csv.reader(file, delimiter=";")

            for row in reader:
                # Skip empty lines as they do not represent students.
                if not row:
                    continue

                # Each line contains three strings; unpack them by position.
                student_id, name, grade_text = row

                # Grades read from CSV are strings, e.g., "89".
                # int() converts it to an integer 89 for comparisons, curving, and summing.
                # Student ID is kept as a string to preserve any potential leading zeros.
                grade = int(grade_text)

                # Parentheses construct a tuple; append adds the student to the local result list.
                students.append((student_id, name, grade))

    except FileNotFoundError:
        # Exception required to be handled: the program should not crash if the file is missing.
        print(f"Error: File not found: {filename}")
        return []

    # Return gives the data back to the caller without printing the list to the screen.
    return students


# ================================
# Task 2: Filtering and Transformations
# ================================

def filter_passing(students):
    """Returns a list of students with grades greater than or equal to 60."""
    passing_students = []

    for student in students:
        # Tuple indices start at 0: 0 is student ID, 1 is name, 2 is grade.
        if student[2] >= 60:
            passing_students.append(student)

    # Creates and returns a new outer list without modifying the input list.
    return passing_students


def to_name_grade_dict(students):
    """Converts a list of student tuples into a {name: grade} dictionary."""
    name_grade_dict = {}

    for student_id, name, grade in students:
        # Unpacks the three elements of each tuple into variables.
        # This task only requires name and grade, so student_id is unused here.
        name_grade_dict[name] = grade

    # For example, returns {"Alice": 89, "Bob": 74}.
    # Dictionary keys are unique; if duplicate names exist, later grades overwrite earlier ones.
    # This reflects the assignment requirement of using names as keys.
    return name_grade_dict


def curve_grades(students, curve_by):
    """Returns a new list of students with curved grades, capped at 100."""
    curved_students = []

    for student_id, name, grade in students:
        # curve_by is the curve amount; passing 5 means adding 5 points to each student.
        # min() caps the grade at 100, so min(grade + curve_by, 100) will never exceed 100.
        new_grade = min(grade + curve_by, 100)

        # Constructs a new student tuple and adds it to the new list.
        # Neither the original students list nor its tuples are modified.
        curved_students.append((student_id, name, new_grade))

    return curved_students


# ================================
# Task 3: Summary Statistics
# ================================

def print_statistics(students):
    """Prints the number of students, average grade, lowest grade, and highest grade with corresponding names matching the assignment format."""
    number_of_students = len(students)
    print(f"Number of students: {number_of_students}")

    # Must handle an empty list first to avoid IndexError on students[0] and ZeroDivisionError for the average.
    # The assignment does not specify empty data formatting; "N/A" is displayed here.
    if number_of_students == 0:
        print("Average grade: N/A")
        print("Lowest grade: N/A")
        print("Highest grade: N/A")
        return

    total_grade = 0

    # Initialize lowest and highest candidates with the first student, then compare iteratively.
    # Storing the entire tuple retains both the grade and the student's name.
    lowest_student = students[0]
    highest_student = students[0]

    for student in students:
        grade = student[2]
        total_grade += grade

        if grade < lowest_student[2]:
            lowest_student = student

        if grade > highest_student[2]:
            highest_student = student

    # Average = total / count. Strict < and > preserve the first occurring student in case of ties.
    average_grade = total_grade / number_of_students

    # f-strings format variables into strings.
    # :.1f formats the float to 1 decimal place, matching the instructor's sample output (e.g., 82.6).
    # It only formats the output and does not alter the underlying numeric value.
    print(f"Average grade: {average_grade:.1f}")
    print(f"Lowest grade: {lowest_student[2]} ({lowest_student[1]})")
    print(f"Highest grade: {highest_student[2]} ({highest_student[1]})")


# ================================
# Task 4: File Writing
# ================================

def write_grades(filename, students):
    """Sorts students alphabetically by name and writes the data to a CSV file."""
    # sorted() returns a new sorted list without modifying the original list.
    # key specifies the sort criterion; here lambda extracts the student's name.
    sorted_students = sorted(students, key=lambda student: student[1])

    # "w" opens the file for writing: creates if missing, overwrites if existing.
    # main uses a distinct filename to preserve the original grades.csv.
    with open(filename, "w", encoding="utf-8", newline="") as file:
        # Uses the same semicolon delimiter as the original file, without adding headers.
        writer = csv.writer(file, delimiter=";")
        writer.writerows(sorted_students)


# ================================
# Task 5: Putting It All Together
# ================================

def main():
    """Workflow: Read -> Statistics -> Filter passing -> Curve +5 -> Statistics -> Save."""
    # __file__ is the current script's path; parent is its enclosing directory.
    # This ensures grades.csv is located relative to the script regardless of working directory.
    script_folder = Path(__file__).resolve().parent

    # Modify input and output filenames here if specified otherwise.
    input_filename = script_folder / "grades.csv"
    output_filename = script_folder / "grades_curved.csv"

    # 1. Read grades from the CSV file. The return value is stored in `students`.
    students = read_grades(input_filename)

    # 2. Print summary statistics for original data.
    print_statistics(students)

    # If the file does not exist or has no students, stop execution to prevent misleading output files.
    if not students:
        return

    # 3. Keep passing students as specified by filter_passing.
    # The instructor's workflow step "Filter failing" means filtering out failing students.
    passing_students = filter_passing(students)

    # 4. Apply a 5-point curve to the filtered students.
    # Filtering before curving prevents previously failing students from re-entering the list.
    curved_students = curve_grades(passing_students, 5)

    # 5. Print statistics for curved grades; a blank line separates the two output sections.
    print()
    print_statistics(curved_students)

    # 6. Sort curved students by name and write to output CSV.
    write_grades(output_filename, curved_students)

    # to_name_grade_dict is implemented above; calling it is not required in the main pipeline.


# When run directly, Python sets __name__ to "__main__" and executes main().
# When imported as a module, main() is not executed, allowing functions to be tested independently.
if __name__ == "__main__":
    main()
