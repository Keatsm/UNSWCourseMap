from flask import Flask, jsonify
from neo4j import GraphDatabase
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

app = Flask(__name__)

# Connect to Neo4j
driver = GraphDatabase.driver(os.getenv("NEO4J_URI"), auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")))

@app.route('/graph', methods=['GET'])
def getGraph():
    # Retrieve nodes from Neo4j
    node_query = "MATCH (n) RETURN n"
    nodes = []

    with driver.session() as session:
        node_result = session.run(node_query)

        for record in node_result:
            node = record['n']
            nodes.append({
                "id": node.id,  # Use node.id directly for the node ID
                "labels": list(node.labels),  # Get the node labels
                "properties": dict(node)  # Get all node properties
            })

    # Retrieve relationships from Neo4j
    relationship_query = "MATCH ()-[r]->() RETURN r"
    relationships = []

    with driver.session() as session:
        relationship_result = session.run(relationship_query)

        for record in relationship_result:
            relationship = record['r']
            relationships.append({
                "startNode": relationship.start_node.id,
                "endNode": relationship.end_node.id,
                "type": relationship.type
            })

    # Create a JSON response with nodes and relationships
    response = {
        "nodes": nodes,
        "relationships": relationships
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)
    print('hello world')
