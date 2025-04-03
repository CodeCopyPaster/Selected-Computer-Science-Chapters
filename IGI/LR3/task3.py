import input_checker
from input_checker import random_input


def task3():
    """
        This function count of spaces and apos in text
    :return: count of spaces and apos
    """

    # Input choose
    choice = input_checker.input_checker("Input:"
                                         "\n1 -> for manual input"
                                         "\n2 -> for auto input", int, 1, 2)

    if choice == 1:
        count_of_space = 0
        count_of_apo = 0
        user_inpur = input_checker.input_checker("Input your text",str)

        for symbol in user_inpur:

            if symbol == " ":
                count_of_space += 1

            elif symbol == "'":
                count_of_apo += 1

        print(f"Count of space: {count_of_space}"
              f"\nCount of apo: {count_of_apo}")

    else:
        count_of_space = 0
        count_of_apo = 0
        random_text = random_input(str,10,20)
        for symbol in random_text:

            if symbol == " ":
                count_of_space += 1

            elif symbol == "'":
                count_of_apo += 1

        print(f"Count of space: {count_of_space}"
             f"\nCount of apo: {count_of_apo}")
