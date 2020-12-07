# by bmitay4
# December 2020
# Sources
# https://stackoverflow.com/questions/59620349/how-to-pass-a-greater-than-or-less-than-sign-through-a-parameter
from typing import List


# Return two maximum values
def choices_max_two(values: List[float]) -> List[bool]:
    choices_list: [bool] = []
    max_value = 0
    second_max_value = 0
    index_max_value = 0
    index_second_max_value = 0
    for index, value in enumerate(values):
        if value >= max_value:
            if max_value > second_max_value:
                second_max_value = max_value
                index_second_max_value = index_max_value
            max_value = value
            index_max_value = index
        elif value >= second_max_value:
            second_max_value = value
            index_second_max_value = index

    for index in range(len(values)):
        if index == index_max_value or index == index_second_max_value:
            choices_list.append(True)
        else:
            choices_list.append(False)

    return choices_list


# Return values over 7
def choices_over_seven(values: List[float]) -> List[bool]:
    choices_list: [bool] = []
    for value in values:
        if value >= 7:
            choices_list.append(True)
        else:
            choices_list.append(False)

    return choices_list


# Gets threshold of an given array's values
def search_threshold_value_over_seven(values: List[float]) -> float:
    # Initialize the threshold value as the biggest value in the vector (from here you can only go down)
    threshold_value = max(values)
    values.sort()

    for index, value in enumerate(values):
        if value <= 7 and 0 < (7 - value) < threshold_value:
            threshold_value = value

    return threshold_value


# Verify that given function is monotony
def monotony_verification(values: List[float], values_choice: List[bool]) -> bool:
    is_monotony = False
    values.sort()

    for index in range(len(values)):
        if values_choice[index] is False and is_monotony:
            raise Exception("Error, The Function Is Not Monotonic")
        elif values_choice[index] is True:
            is_monotony = True
        else:
            values[index] = 0

    return is_monotony


def payments(values: List[float]) -> List[float]:
    threshold_value = search_threshold_value_over_seven(values)
    choices_players = choices_over_seven(values)
    print("Array Sorted: ", values)
    # We will make sure the function is monotonous, otherwise we will end the program
    try:
        monotony_verification(values, choices_players)
    except Exception as e:
        print(e)
        exit(1)

    payment_values: [float] = []

    for index, value in enumerate(values):
        if value != 0:
            payment_values.append(threshold_value)
        else:
            payment_values.append(0)

    return payment_values


if __name__ == '__main__':
    players_1 = [5, 6, 3, 7, 8]
    players_2 = [10, 6, 6, 8, 9]

    print("Value Over 7 Choice, Given Array: ", players_1)
    print("Final Payments: ", payments(players_1))
    print("-------------------------")

    print("Value Over 7 Choice, Given Array: ", players_2)
    print(payments(players_2))
    print("-------------------------")
