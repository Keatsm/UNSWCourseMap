from flask import Flask, jsonify
from neo4j import GraphDatabase
from dotenv import load_dotenv, find_dotenv
import os, json
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="https://unsw-course-map.vercel.app")

load_dotenv(find_dotenv())

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

# Connect to Neo4j
driver = GraphDatabase.driver(os.getenv("NEO4J_URI"), auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")))

@app.route('/graph', methods=['GET'])
def getGraph():
    # Retrieve nodes from Neo4j
    node_query = "MATCH (n) RETURN n"
    nodes = []

    try:
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

        result = {
            "nodes": nodes,
            "relationships": relationships
        }
        with open('cache.json', 'w') as file:
            json.dump(result, file, indent=4)
    except:
        with open('cache.json', 'r') as file:
            result = json.load(file)

    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    print('hello world')
