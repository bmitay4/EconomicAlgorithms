# November 2020
# by bmitay4

# Sources
# https://stackoverflow.com/questions/60397606/how-to-round-off-values-corresponding-to-edge-labels-in-a-networkx-graph
# https://www.programmersought.com/article/1688631551/
# https://matplotlib.org/2.0.1/examples/pylab_examples/annotation_demo2.html

from typing import List
import networkx as nx
import matplotlib.pyplot as plt


class Agent:
    def __init__(self, values: List):
        self.values_list = values

    def item_value(self, item_index: int) -> float:
        return self.values_list[item_index]


def get_values(agent: Agent, agent_index: int, bundles: List[List[int]]) -> float:
    items_value = 0
    for item in bundles[agent_index]:
        items_value = items_value + agent.item_value(item)
    return items_value


def envy_graph(agents: List[Agent], bundles: List[List[int]]):
    envy_free_graph = nx.DiGraph()

    for agent_index, agent in enumerate(agents):
        envy_free_graph.add_node("Agent {}".format(agent_index + 1))

    for agent_idx, agent in enumerate(agents):
        agent_values = get_values(agent, agent_idx, bundles)
        for bundle_idx, bundle in enumerate(bundles):
            agent_other_values = 0
            for item in bundle:
                agent_other_values = agent_other_values + agent.item_value(item)
            if agent_other_values > agent_values:
                envy_free_graph.add_edge("Agent {}".format(agent_idx + 1), "Agent {}".format(bundle_idx + 1))

    pos = nx.spring_layout(envy_free_graph)
    nx.draw(envy_free_graph, pos, node_color='skyblue', with_labels=True, connectionstyle='arc3, rad = 0.1')
    plt.show()


if __name__ == '__main__':
    # Everyone is jealous of the other, an example from the lecture
    agents_list = [Agent([1, 3, 2]), Agent([2, 1, 3]), Agent([3, 2, 1])]
    bundles_list = [[0], [1], [2]]

    envy_graph(agents_list, bundles_list)

    # Everyone has the same preferences, no one is jealous of another
    agents_list_1 = [Agent([5, 5, 5]), Agent([5, 5, 5]), Agent([5, 5, 5])]
    bundles_list_1 = [[0], [1], [2]]

    envy_graph(agents_list_1, bundles_list_1)

    # Three jealous of the first player
    agents_list_2 = [Agent([1, 5, 0]), Agent([0, 4, 0]), Agent([0, 4, 0]), Agent([0, 4, 0])]
    bundles_list_2 = [[0, 1], [2], [2], [2]]

    envy_graph(agents_list_2, bundles_list_2)
