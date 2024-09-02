from neo4j import GraphDatabase, RoutingControl, basic_auth

URI = "bolt://44.201.125.41:7687"
AUTH = basic_auth("neo4j", "counsels-pictures-abuser")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.execute_query(
        """
MATCH (n)
RETURN COUNT(n) AS count
LIMIT $limit
"""
    )
