from getPages import getPages
from createGraph import createGraph
import matplotlib.pyplot as plt
import networkx as nx
from dotenv import load_dotenv
import os
from neo4j import GraphDatabase
import logging
import sys
from py2neo import Graph

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logging.getLogger("neo4j").addHandler(handler)
logging.getLogger("neo4j").setLevel(logging.DEBUG)

load_dotenv()

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

session = Graph(uri, auth=(username, password))

def clearDB():
    session.run("MATCH (n) DETACH DELETE n")

def addGraphToDB(graph):
    for node, data in graph.nodes(data=True):
        session.run("CREATE (n:Node {id: $id, attributes: $attrs})", id=node, attrs=data['attr'])
    
    for edge in graph.edges():
        session.run("MATCH (a:Node {id: $src}), (b:Node {id: $dest}) "
                    "CREATE (a)-[:CONNECTED]->(b)", src=edge[0], dest=edge[1])

if __name__ == '__main__':
    clearDB()
    graph = createGraph(getPages())
    addGraphToDB(graph)
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()