import cvxpy
import numpy


def calculate_pareto_efficiency(input_matrix: numpy.ndarray):
    # Variables which holding agents and the resources amount
    rows = input_matrix.shape[0]
    columns = input_matrix.shape[1]
    variable_count = get_variables_count(rows, columns, input_matrix)

    if variable_count == 0:  # No Envy At All!
        x = cvxpy.Variable()
        problem = cvxpy.Problem(cvxpy.Maximize(cvxpy.log((81 + 19) ** 0.5) + cvxpy.log((80 + 20) ** 0.5)),
                                constraints=[0 <= x, x <= 1])
        problem.solve()

        print("Agent #1 gets", x.value, "of all resources")
        print("Agent #2 gets", 1 - x.value, "of all resources")
    elif variable_count == 1:  # Envy exists, 2 or more agents are interested in the same resource
        x = cvxpy.Variable()
        problem = cvxpy.Problem(cvxpy.Maximize(cvxpy.log((81 * x + 19) ** 0.5) + cvxpy.log((80 * (1 - x) + 20) ** 0.5)),
                                constraints=[0 <= x, x <= 1])
        problem.solve()

        print("Agent #1 gets", x.value, "of resource #1, 1.0 of resource #2, and 0.0 of resource #3")
        print("Agent #2 gets", 1 - x.value, "of resource #1, 0.0 of resource #2, and 1.0 of resource #3")
    else:  # Envy exists, 2 or more agents are interested in common in more than one resource
        x = cvxpy.Variable()
        y = cvxpy.Variable()

        problem = cvxpy.Problem(cvxpy.Maximize(cvxpy.log((81 * x + 19) ** 0.5) + cvxpy.log((80 * (1 - x) + 20) ** 0.5)),
                                constraints=[0 <= x, x <= 1])
        problem.solve()

        print("Agent #1 gets", x.value, "of resource #1, 1.0 of resource #2, and 0.0 of resource #3")
        print("Agent #2 gets", 1 - x.value, "of resource #1, 0.0 of resource #2, and 1.0 of resource #3")

    # x = cvxpy.Variable()
    # problem = cvxpy.Problem(cvxpy.Maximize(cvxpy.log((81 * x + 19) ** 0.5) + cvxpy.log((80 * (1 - x) + 20) ** 0.5)),
    #                         constraints=[0 <= x, x <= 1])
    # problem.solve()
    #
    # print("status:", problem.status)
    # print("optimal value: ", problem.value)
    # print("optimal value: ", x.value)
    # print("optimal value: ", 1 - x.value)

    # print("Agent #1 gets", x.value, "of resource #1, 1.0 of resource #2, and 0.0 of resource #3")
    # print("Agent #2 gets", 1 - x.value, "of resource #1, 0.0 of resource #2, and 1.0 of resource #3")


def get_temp_matrix(input_matrix: numpy.ndarray):
    rows = input_matrix.shape[0]
    columns = input_matrix.shape[1]

    temp_matrix = numpy.arange(rows * columns, dtype=int).reshape(rows, columns)

    for row in range(rows):
        for column in range(columns):
            if input_matrix[row, column] == 0:
                temp_matrix[row, column] = -1
            else:
                temp_matrix[row, column] = input_matrix[row, column]

    return temp_matrix


def get_variables_count(rows: int, columns: int, input_matrix: numpy.ndarray):
    count = 0
    for row in range(rows - 1):
        for column in range(columns):
            if input_matrix[row, column] != 0 and input_matrix[row + 1, column] != 0:
                count = + 1
    return count


if __name__ == '__main__':
    # Define a matrix for holding the resources
    matrix = numpy.array([[81, 19, 0], [80, 0, 20]])

    calculate_pareto_efficiency(matrix)
