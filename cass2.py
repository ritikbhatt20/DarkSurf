from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# Set the keyspace
session.set_keyspace('employee')

# Create a table
table_query = """
    CREATE TABLE IF NOT EXISTS details (
        user_id UUID PRIMARY KEY,
        username text,
        email text,
        age int
    );
"""
session.execute(table_query)

# Insert data into the table
insert_query = """
    INSERT INTO details (user_id, username, email, age) VALUES (
        UUID(), 'john_doe', 'john.doe@example.com', 30
    );
"""
session.execute(insert_query)

# Query data from the table
select_query = "SELECT * FROM details;"
result = session.execute(select_query)

print("Data in the 'details' table:")
for row in result:
    print(row.user_id, row.username, row.email, row.age)

# Close the connection
cluster.shutdown()
