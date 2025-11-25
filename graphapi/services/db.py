#la connexion au driver Neo4j
from py2neo import Graph
import os

def get_graph():
    return Graph(
        os.getenv("NEO4J_URI"),
        auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
    )
