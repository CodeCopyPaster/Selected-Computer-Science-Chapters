import input_checker

def process_list(numbers: list):
    def non_zero_indices():
        for i, num in enumerate(numbers):
            if num != 0:
                yield i

    max_value = max(numbers)
    max_index = numbers.index(max_value)
    print(f"Index of the greatest number: {max_index}")

    nz_indices = non_zero_indices()
    first_non_zero_index = next(nz_indices, None)
    second_non_zero_index = next(nz_indices, None)

    if first_non_zero_index is not None and second_non_zero_index is not None:
        product = 1
        for num in numbers[first_non_zero_index + 1:second_non_zero_index]:
            product *= num
        print(f"Product between two non-zero numbers: {product}")
    else:
        print("There are not enough non-zero numbers.")

def task5():
    """
        This function find index of the greatest number, product of two non-zero numbers
    :return:
    """

    # Input choose
    choice = input_checker.input_checker("Input:"
                                         "\n1 -> for manual text"
                                         "\n2 -> for random input", int, 1, 2)

    listik = []
    if choice == 1:

        count_user_input = input_checker.input_checker("Input count of numbers for list to check",int,1)

        while count_user_input:
            user_input = input_checker.input_checker("Input num for the list",int)
            listik.append(user_input)
            count_user_input -= 1

        process_list(listik)

    else:
        random_count_of_numbers = input_checker.random_input(int,5,15)
        while random_count_of_numbers:
            random_input = input_checker.random_input(int,-50,50)
            listik.append(random_input)
            random_count_of_numbers -= 1

        process_list(listik)
