import input_checker

def task2():
    """
        This funstion calculate count of numbers from 5 to 25
    :return:count of numbers between 5 and 25
    """

    choice = input_checker.input_checker("Input:"
                                         "\n1 -> for manual input"
                                         "\n2 -> for auto input", int, 1, 2)

    if choice == 1:
        count = 0
        while True:
            user_input = input_checker.input_checker("Input your number, input 0 to stop", (float,int))

            if user_input >= 5 or user_input <= 25:
                count += 1
            elif user_input == 0:
                print(f"Count of numebrs beetwen 5 and 25 is: {count}")
                break

    else:
        count = 0
        count_of_random_value = input_checker.random_input(int,10,20)

        while count_of_random_value:
            random_value = input_checker.random_input(int, -100, 100)

            if random_value >= 5 or random_value <= 25:
                count += 1
                count_of_random_value -= 1

        print("Auto stop")

        #Display results
        print(f"Count of numebrs beetwen 5 and 25 is: {count}")



