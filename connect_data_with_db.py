from neo4j import GraphDatabase, RoutingControl, basic_auth

URI = "bolt://44.201.125.41:7687"
AUTH = basic_auth("neo4j", "counsels-pictures-abuser")

# Add bank clients
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.execute_query(
        """
LOAD CSV WITH HEADERS FROM
'https://filebin.net/gqjzspyvcvirrxvu/bank_customer.csv' AS row
MERGE (client:Client { id: row.id, name: row.name, birthdate: row.birthdate, gender: row.gender, address: COALESCE(row.address, '') })
RETURN row
LIMIT 5;
"""
    )

# Add clients accounts
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.execute_query(
        """
LOAD CSV WITH HEADERS FROM
'https://filebin.net/gqjzspyvcvirrxvu/bank_accounts.csv' AS row
MERGE (account:Account { id: row.id, type: row.type, balance: row.balance, currency: row.currency })
MERGE (client:Client { id: row.client_id })
MERGE (client)-[:HAS]->(account)
RETURN row
LIMIT 5;
"""
    )

# Add accounts transactions
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.execute_query(
        """
LOAD CSV WITH HEADERS FROM
'https://filebin.net/gqjzspyvcvirrxvu/bank_transactions.csv' AS row
MERGE (originAccount:Account { id: row.from_account })
MERGE (destinationAccount:Account { id: row.to_account })
MERGE (originAccount)-[:MADE_A_TRANSACTION { id: row.id, date: row.date, method: row.method, method_id: COALESCE(row.method_id, '') }]->(destinationAccount)
RETURN row
LIMIT 5;
"""
    )

# Add cards transactions
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.execute_query(
        """
LOAD CSV WITH HEADERS FROM
'https://filebin.net/gqjzspyvcvirrxvu/bank_cards.csv' AS row
MERGE (client:Client { id: row.client_id })
MERGE (card:CreditCard { id: row.id,number: row.number,security_code: row.security_code,provider: row.provider,expiration_date: row.expiration_date})
MERGE (client)-[:OWNS]->(card)
RETURN row
LIMIT 5;
"""
    )


# Pegar cliente que usou pix pelo menos uma vez
# MATCH (client:Client)-[:HAS]->(:Account)-[:MADE_A_TRANSACTION { method: "pix"}]->(:Account) RETURN client LIMIT 10

# Pegar cliente que fez mais de 1 pix
# MATCH (client:Client)-[:HAS]->(a:Account)-[r:MADE_A_TRANSACTION { method: "pix"}]->(b:Account) WITH client, a, b, count(r) as rel_cnt
# WHERE rel_cnt > 1 RETURN client  LIMIT 10
