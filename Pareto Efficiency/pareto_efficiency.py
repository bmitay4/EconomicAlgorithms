import cvxpy
import numpy

global matrix


def calculate_pareto_efficiency(input_matrix: numpy.ndarray):
    global matrix
    matrix = input_matrix

    # Verify that matrix value are non negative
    matrix_validation()

    # Create variables for the functions for each user (matrix's rows)
    variables_list = get_variables()

    # Get matrix's index of max value
    index_max_value = get_max_value()

    # If there is no envy, we can skip some of the processes
    if len(index_max_value) != 0:
        # Calculate each log for each matrix cell, then combine it all
        logs_values = get_logs_values(index_max_value, variables_list)

        # We will force the algorithm to take into account the sum of the variables
        # which must be 1 in order to achieve effective optimization
        constrains_values = get_constrains(variables_list)

        # Calculate the values
        get_calculation(logs_values, constrains_values)

    # Prints the result
    to_string(index_max_value, variables_list)


def matrix_validation():
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            if matrix[row][column] < 0:
                raise ValueError('Error. Matrix includes non-negative values. Check the input and try again.')


def get_variables():
    variable_list = []
    for row in range(len(matrix)):
        variable_list.append(cvxpy.Variable())
    return numpy.array(variable_list)


def get_max_value():
    topValues = []
    for row in range(len(matrix) - 1):
        for column in range(len(matrix[0])):
            if matrix[row][column] != 0 and matrix[row + 1][column] != 0:
                topValues.append(column)
    return topValues


def get_logs_values(index_max_value, variable_list):
    logs_values = []
    total_logs_sum = 0
    for row in range(len(matrix)):
        single_log = 0
        for column in range(len(matrix[0])):
            for value in index_max_value:
                if column == value:
                    single_log += variable_list[row] * matrix[row][column]
                else:
                    single_log += matrix[row][column]
        logs_values.append(cvxpy.log(single_log))

    logs_values = numpy.array(logs_values)
    for value in range(len(logs_values)):
        total_logs_sum = total_logs_sum + logs_values[value]

    return total_logs_sum


def get_constrains(variable_list):
    constrains_list = []
    sum_constrains = 0
    for variable in variable_list:
        constrains_list.append(0 <= variable)
        constrains_list.append(variable <= 1)

        sum_constrains += variable

    constrains_list.append(sum_constrains == 1)
    return constrains_list


def get_calculation(logs_values, constrains_values):
    problem = cvxpy.Problem(cvxpy.Maximize(logs_values), constrains_values)
    problem.solve()


def to_string(index_max_value, variable_list):
    if len(index_max_value) == 0:
        for row in range(len(matrix)):
            print("Agent #{} gets".format(row + 1), end=" ")
            for column in range(len(matrix[0])):
                print("{} of resource #{},".format(1.0 if matrix[row][column] != 0 else 0, column + 1), end=" ")
            if row + 1 != len(matrix):
                print()
    else:
        for value in index_max_value:
            for row in range(len(matrix)):
                print("Agent #{} gets".format(row + 1), end=" ")
                flag:bool = False
                for column in range(len(matrix[0])):
                    if column == value:
                        print("{} of resource #{},".format(variable_list[row].value, column + 1), end=" ")
                    else:
                        print("{} of resource #{},".format(1.0 if matrix[row][column] != 0 else 0, column + 1), end=" ")
                if row + 1 != len(matrix):
                    print()


if __name__ == '__main__':
    # Define matrices for holding the resources
    matrix_1 = numpy.array([[81, 19, 0], [80, 0, 20]])
    matrix_1_1 = numpy.array([[81, 19, 0], [80, 0, 20], [80, 0, 0]])
    matrix_1_1_1 = numpy.array([[81, 19, 0, 0], [80, 0, 20, 0], [30, 0, 0, 0]])
    matrix_2 = numpy.array([[19, 0, 81], [0, 20, 80]])
    matrix_3 = numpy.array([[0, 81, 19], [20, 80, 0]])
    matrix_4 = numpy.array([[81, 50, 0], [81, 10, 30]])

    error_matrix = numpy.array([[-1, 0, 81], [0, 20, 80]])

    calculate_pareto_efficiency(matrix_1_1)
