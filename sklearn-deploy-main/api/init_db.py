import psycopg2

def create_database():
    try:
        # Connect to the default PostgreSQL database
        connection = psycopg2.connect(
            user="your_username",
            password="your_password",
            host="localhost",
            port="5432",
            database="postgres"
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Create a new database named 'defaultdb'
        cursor.execute("CREATE DATABASE defaultdb;")

        # Close the cursor and connection to the default database
        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL or creating the database:", error)

def initialize_database():
    try:
        # Connect to the 'defaultdb' database
        connection = psycopg2.connect(
            user="your_username",
            password="your_password",
            host="localhost",
            port="5432",
            database="defaultdb"
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Read the schema from the 'schema.sql' file
        with open("schema.sql", "r") as file:
            schema = file.read()

        # Execute the schema to create tables
        cursor.execute(schema)

        # Commit the changes and close the cursor and connection
        connection.commit()
        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL or initializing the database:", error)

