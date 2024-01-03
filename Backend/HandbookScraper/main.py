from getPages import getPages
from createGraph import createGraph
import matplotlib.pyplot as plt
import networkx as nx
from dotenv import load_dotenv, find_dotenv
import os
from py2neo import Graph


load_dotenv(find_dotenv())

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

session = Graph(uri, auth=(username, password))

def clearDB():
    session.run("MATCH (n) DETACH DELETE n")

def addGraphToDB(graph):
    for node, data in graph.nodes(data=True):
        # Translate the data dictionary to primitive values
        attrPrimitive = {
            key: value if not isinstance(value, (dict, list)) else str(value)
            for key, value in data['attr'].items()
        }
        if not attrPrimitive['specialNode']:
            attrPrimitive['label'] = node
        query = (
            "CREATE (n:MyNode {id: $id, "
            + ", ".join([f"{key}: ${key}" for key in attrPrimitive])
            + "})"
        )
        session.run(query, id=node, **attrPrimitive)
    
    for edge in graph.edges():
        session.run("""MATCH (a:MyNode {id: $src}), (b:MyNode {id: $dest})
                    CREATE (a)-[:REQUIRES]->(b)""", src=edge[0], dest=edge[1])

if __name__ == '__main__':
    clearDB()
    
    graph = createGraph(getPages())
    addGraphToDB(graph)
    
    # Visualize the graph
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()