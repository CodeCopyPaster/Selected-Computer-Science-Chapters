import math
import input_checker


def task1():

    """
        This function will calculate ln(x-1) using series decomposition,
        compare with math.ln(x-1).
    """
    MAX_ITERATIONS = 500

    # Input choose
    choice = input_checker.input_checker("Input:"
                                         "\n1 -> for manual input"
                                         "\n2 -> for auto input", int, 1, 2)

    if choice == 1:
        # Manual input
        while True:
            x = input_checker.input_checker("Input \'x\' greater than 1: ", float, 1)
            if x == -1 or x == 1:
                print("\'x\' must not be lower than 1")
            else:
                break

        eps = input_checker.input_checker("Input \'eps\' from 0 to 1: ", float, 1e-10, 1)

    else:
        # Auto input
        x = input_checker.random_input(float, 1, 2)
        eps = input_checker.random_input(float, 1e-10, 0.1)

    # Calculating ln(x-1) with decomposition
    y = x - 2  # Shift to center around 1
    if abs(y) >= 1:
        raise ValueError("Series only converges for 1 < x < 3")

    result = 0.0
    for n in range(1, MAX_ITERATIONS + 1):
        term = (-1) ** (n + 1) * (y ** n) / n
        result += term
        if abs(term) < eps:
            break


    # Value from math library
    math_value = math.log(x-1)

    # Display results
    print("\nResults:")
    print("|----------------------------------------------------|")
    print("|    x    |  n  |    F(x)    | Math F(x)  |   eps    |")
    print("|---------|-----|------------|------------|----------|")
    print(f"| {x:7.4f} | {n + 1:3} | {result:0.3f} | {math_value:0.3f} | {eps:8.2e} |")
    print("|----------------------------------------------------|")
