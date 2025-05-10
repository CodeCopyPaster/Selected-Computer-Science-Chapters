import input_checker
import task1
import task2
import task3
import task4
import task5
import dopka

def main():
    """"
       Main function to choose task num.
    """

    while True:
        print("==MENU==")
        print("Task 1")
        print("Task 2")
        print("Task 3")
        print("Task 4")
        print("Task 5")
        print("Task 6 (dop zadanie)")
        print("Exit (0)")

        user_choice = input_checker.input_checker("Input num of task or 0 to exit ", int, 0, 6)

        if user_choice == 1:
            task1.task1()

        elif user_choice == 2:
            task2.task2()

        elif user_choice == 3:
            task3.task3()

        elif user_choice == 4:
            task4.task4()

        elif user_choice == 5:
            task5.task5()

        elif user_choice == 6:
            dopka.doptask()

        elif user_choice == 0:
            print("Exit")
            break


if __name__ == "__main__":
    main()