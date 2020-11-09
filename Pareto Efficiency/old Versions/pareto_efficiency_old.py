import cvxpy
import numpy


class ParetoEfficiency:
    def __init__(self, input_matrix: numpy.ndarray):
        self.matrix = input_matrix
        self.agents = []
        self.variables_array = []
        self.rows = -1
        self.columns = -1
        self.variables_count = -1

    def configuration(self):
        self.agents = self.agents_list()
        self.variable_sum()
        self.rows = len(self.agents) - 1
        self.columns = len(self.agents[0])
        self.variables_count = len(self.agents[len(self.agents) - 1])
        self.variables_array = self.agents[len(self.agents) - 1]

    def agents_list(self):
        temp_list = []
        for row in range(self.matrix.ndim):
            temp_list.append(self.agent_array(row))
        return temp_list

    def agent_array(self, index: int):
        temp_list = []
        for cell in self.matrix[index]:
            temp_list.append(cell)
        return temp_list

    def variable_sum(self):
        temp_list = []
        for row in range(len(self.agents) - 1):
            for column in range(len(self.agents[0])):
                if self.agents[row][column] != 0 and self.agents[row + 1][column] != 0:
                    temp_list.append(column)
        self.agents.append(temp_list)

    def calculate_pareto_efficiency(self):
        self.get_info()
        self.matrix_validation()

        if self.variables_count == 0:
            print("No Envy At All!\n")

            x = cvxpy.Variable()

            total_logs: cvxpy.Expression = 0

            for index in range(self.rows):
                total_logs += (self.calculate_values(x, self.agents[index], index))
            # print(total_logs)
            problem = cvxpy.Problem(cvxpy.Maximize(total_logs), constraints=[0 <= x, x <= 1])
            problem.solve()

            print("Agent #1 gets", x.value, "of all resources")
            print("Agent #2 gets", 1 - x.value, "of all resources")

        elif self.variables_count == 1:
            print("Envy exists, two or more agents are interested in a same resource\n")
            x = cvxpy.Variable()
            total_logs: cvxpy.Expression = 0

            for index in range(self.rows):
                total_logs += (self.calculate_values(x, self.agents[index], index))
            # print(total_logs)
            problem = cvxpy.Problem(cvxpy.Maximize(total_logs), constraints=[0 <= x, x <= 1])
            problem.solve()
            print(problem.value)
            self.to_string(x)

        else:
            print("Envy exists, two or more agents are interested in common in more than one resource")

    def calculate_values(self, x: cvxpy.Variable, agent: list, index: int):
        count = 0
        agent_sum: cvxpy.log = 0
        if len(self.variables_array) > 0:
            for variable in range(len(self.variables_array)):
                for value in agent:
                    if self.variables_array[variable] == count and index % 2 == 0:
                        agent_sum += value * x
                    elif self.variables_array[variable] == count and index % 2 == 1:
                        agent_sum += value * (1 - x)
                    elif value != 0:
                        agent_sum += value
                    count += 1
        else:
            for value in agent:
                if value != 0 and index % 2 == 0:
                    agent_sum += value * x
                elif value != 0 and index % 2 == 1:
                    agent_sum += value * (1 - x)
        return cvxpy.log(agent_sum ** 0.5)

    # Check if matrix's values are non negative
    def matrix_validation(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.agents[row][column] < 0:
                    raise ValueError('Error. Matrix includes non-negative values. Check the input and try again.')

    # toString, prints the output of the calculation
    def to_string(self, x: cvxpy.Variable):
        p_value = self.variables_array[0] + 1
        np_valuea = -1
        np_valueb = -1
        for index in range(self.columns):
            if p_value != index + 1:
                if np_valuea == -1:
                    np_valuea = index + 1
                elif np_valueb == -1:
                    np_valueb = index + 1

        for index in range(self.rows):
            if index % 2 == 0:
                print("Agent #", index + 1, "gets", x.value, "of resource #", p_value,
                      ", 1.0 of resource #", np_valuea, ",and 0.0 of resource #", np_valueb)
            else:
                print("Agent #", index + 1, "gets", 1 - x.value, "of resource #", p_value,
                      ", 1.0 of resource #", np_valuea, ",and 0.0 of resource #", np_valueb)

    # Prints info about the given matrix including the agents and the resources
    def get_info(self):
        print("------------------------")
        print("Current Matrix: ", self.matrix)
        print("Amount Of Agents (Rows): ", self.rows)  # Rows
        print("Amount Of Resources (Resources):", self.columns)  # Columns
        print("Amount Of cvxpy Variables Needed:", self.variables_count)
        print("Preferred Resources At Indexes: ", self.variables_array)
        print("------------------------")
        print()


if __name__ == '__main__':
    # Define matrices for holding the resources
    matrix_1 = numpy.array([[81, 19, 0], [80, 0, 20]])
    matrix_2 = numpy.array([[19, 0, 81], [0, 20, 80]])
    matrix_3 = numpy.array([[0, 81, 19], [20, 80, 0]])
    myObj = ParetoEfficiency(matrix_1)

    matrix_4 = numpy.array([[50, 0, 20], [50, 0, 20]])
    # myObj = ParetoEfficiency(matrix_4)

    no_envy_matrix = numpy.array([[100, 100, 0], [0, 0, 10]])
    # myObj = ParetoEfficiency(no_envy_matrix)

    error_matrix = numpy.array([[-1, 0, 81], [0, 20, 80]])
    # myObj = ParetoEfficiency(error_matrix)

    myObj.configuration()
    myObj.calculate_pareto_efficiency()
