
from neo4j import GraphDatabase, basic_auth

driver = GraphDatabase.driver(
  "bolt://44.203.242.88:7687",
  auth=basic_auth("neo4j", "lumps-electrodes-indication"))

cypher_query = '''
MATCH (n)
RETURN COUNT(n) AS count
LIMIT $limit
'''

with driver.session(database="neo4j") as session:
  results = session.read_transaction(
    lambda tx: tx.run(cypher_query,
                      limit="10").data())
  for record in results:
    print(record['count'])

driver.close()
