from cassandra.cluster import Cluster

cluster = None
session = None

try:
    # Connect to Cassandra Docker container with the container name
    print("Connecting to Cassandra...")
    cluster = Cluster(['cass_clusterr'], port=9042, control_connection_timeout=10, connect_timeout=10)
    session = cluster.connect()

    # Use the keyspace 'ritik'
    keyspace_query = "USE ritik"
    session.execute(keyspace_query)

    # Create a table if it doesn't exist
    create_table_query = """
        CREATE TABLE IF NOT EXISTS lol (
            user_id UUID PRIMARY KEY,
            age INT,
            email TEXT,
            username TEXT
        )
    """
    session.execute(create_table_query)

    # Insert data into the table
    insert_data_query = """
        INSERT INTO lol (user_id, age, email, username) VALUES (uuid(), 30, 'john.doe@example.com', 'john_doe')
    """
    session.execute(insert_data_query)

    # Query data from the table
    select_data_query = "SELECT * FROM lol"
    rows = session.execute(select_data_query)

    # Display the results
    for row in rows:
        print(f"User ID: {row.user_id}, Age: {row.age}, Email: {row.email}, Username: {row.username}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the connection
    try:
        if session:
            session.shutdown()
    except Exception as e:
        print(f"Error while closing session: {e}")

    try:
        if cluster:
            cluster.shutdown()
    except Exception as e:
        print(f"Error while closing cluster: {e}")




