from getPages import getPages
from createGraph import createGraph
import matplotlib.pyplot as plt
import networkx as nx

if __name__ == '__main__':
    graph = createGraph(getPages())
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()