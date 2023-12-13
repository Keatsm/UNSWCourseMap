from getPages import getPages
from createGraph import createGraph

if __name__ == '__main__':
    graph = createGraph(getPages())
    print(graph)