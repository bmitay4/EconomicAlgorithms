# November 2020
# by bmitay4

import random
import numpy as np
import networkx as nx


def calculate_rental_harmony(matrix: np.ndarray):
    print("Initial Matrix:\n", matrix, "\n")

    # Variable which holds the matrix's dimensions
    questions = len(matrix[0])
    students = len(matrix)
    partial_value = int(questions / students)

    # Define an empty complete bipartite graph
    G = nx.complete_bipartite_graph(0, 0)

    # Defining vertex groups
    students_nodes = []
    questions_nodes = []

    # Filling vertex groups, one group will be the vertices of the students,
    # and the other group will be the vertices of the question number
    for row in range(len(matrix)):
        students_nodes.append("Student " + str(row + 1))
    for column in range(questions):
        questions_nodes.append("Question " + str(column + 1))

    # Assign the vertex groups to the graph
    G.add_nodes_from(students_nodes, bipartite=1)
    G.add_nodes_from(questions_nodes, bipartite=0)

    # Filling vertex groups, each cell describes the level of effort of the
    # student in a row, for the question in the column, multiply by -1
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            G.add_weighted_edges_from([(students_nodes[row], questions_nodes[column], -1 * matrix[row][column])])

    # For all edges in the graph, search for the edges with the lowest weights,
    # and insert it to the ans array, until the number of edges remains as the number of questions (matrix columns)
    ans = []
    while len(ans) < questions:
        min_weights = nx.max_weight_matching(G, True)
        for u, v in nx.max_weight_matching(G, True):
            if u.__contains__("Question"):
                ans.append(str(v) + " :" + str(u)[8:])
                for nodes in (list(G.neighbors(u))):
                    if nodes is not v:
                        G.remove_edge(nodes, u)
            else:
                ans.append(str(u) + " :" + str(v)[8:])
                for nodes in (list(G.neighbors(v))):
                    if nodes is not u:
                        G.remove_edge(nodes, v)
        G.remove_edges_from(min_weights)

    # Convert the array to a sorted numpy array (Descending)
    ans = np.array(sorted(ans))

    # Print the total effort's sum for each student
    print("The divide questions for each student:\n", ans, "\n")
    for row in range(students):
        student_sum = 0
        for value in range(partial_value * row, partial_value * row + partial_value):
            student_sum += matrix[row][int(str(ans[value])[12:]) - 1]
        print("For student {}, Total effort for questions is: {}".format(row + 1, student_sum))


def random_values(students: int, questions: int, min_value: int, max_value: int):
    if questions % students != 0:
        raise Exception("Error, recheck your input\n"
                        "There is no equal division between the amount of questions and the students")

    single_row = []
    ans = []
    for row in range(students):
        for column in range(questions):
            single_row.append(random.randint(min_value, max_value))
        ans.append(single_row)
        single_row = []
    return ans


if __name__ == '__main__':
    # Defines the effort level for each of the twelve questions (range 1-5)
    students_1 = [[0, 0, 0, 0, 5, 4, 3, 2, 2, 2, 1, 1],
                  [5, 5, 2, 3, 0, 0, 0, 0, 2, 4, 3, 2],
                  [1, 2, 1, 1, 2, 5, 4, 1, 0, 0, 0, 0]]

    students_2 = [[2, 3, 4, 5, 5, 4, 3, 2, 2, 2, 1, 1],
                  [5, 5, 2, 3, 4, 1, 2, 3, 1, 4, 3, 2],
                  [1, 2, 1, 1, 2, 5, 4, 1, 3, 3, 5, 5]]

    # Added during class
    students_segal = [[2, 3, 4, 5, 5, 4, 3, 2, 2],
                      [5, 5, 2, 3, 4, 1, 2, 3, 4]]

    # Random array, by: (Students, Questions, Min random value, Max random value)
    random_students = random_values(2, 4, 0, 10)

    students_3 = [[4, 1, 5, 4, 5, 1, 2, 3, 4, 5, 1, 1],
                  [1, 3, 4, 5, 1, 4, 3, 4, 5, 4, 5, 5],
                  [3, 4, 1, 1, 2, 5, 4, 5, 1, 2, 3, 4]]

    students_4 = [[5, 0, 1, 2, 5, 3, 3, 3, 1, 1, 5, 5],
                  [1, 1, 1, 1, 2, 2, 2, 2, 5, 4, 5, 5],
                  [1, 2, 5, 4, 2, 0, 1, 0, 5, 5, 5, 5]]

    calculate_rental_harmony(np.array(random_students))
