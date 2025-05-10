import random, string

def input_checker(promt, type_of_data, min_value = None, max_value = None):
    """
        This function check user input for tasks.

    :param promt: user's input
    :param type_of_data: type of user promt data
    :param min_value: minimum required value for task
    :param max_value: maximum required value for task
    :return: valid user's input OR error
    """

    while True:
        try:
            users_input = type_of_data(input(promt))

            if min_value is not None and users_input < min_value:
                raise ValueError(f"Input value greater or equal than {min_value}")

            elif max_value is not None and users_input > max_value:

                raise ValueError(f"Input value lower or equal than {min_value}")
            return users_input;

        except ValueError:
            print(f"Errros : {ValueError}. Please enter one more time");

def random_input(required_datatype, min_value=None, max_value=None):
    """
        This function generate random value for task.

    :param datatype: required type of data
    :param min_value: minimum required value for task
    :param max_value: maximum required value for task
    :return: random value
    """

    if required_datatype == int:
        generated_value = random.randint(min_value,max_value)

    elif required_datatype == float:
        generated_value = random.uniform(min_value,max_value)

    elif required_datatype == str:
        if min_value is None:
            min_value = 1

        if max_value is None:
            max_value = 50

        generated_value = ''.join(random.choices(
            string.ascii_letters + string.digits,
            k=random.randint(min_value, max_value)
        ))
    else:
        raise ValueError("Unused type of data for tasks, use: int, float, str")

    return generated_value