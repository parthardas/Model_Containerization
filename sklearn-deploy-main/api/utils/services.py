'''
db connection creation
and other crud operations for inserting data into the database
'''
import os
import psycopg2

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DBNAME = os.getenv('DBNAME')

def connect_to_database():
    try:
        # Connect to the database
        connection = psycopg2.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=DBNAME
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None

def insert_user(connection, user_data):
    if not connection: return None, ValueError
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s)", user_data)
        cursor = connection.cursor()
        cursor.close()
        return user_data[0], None
    except (Exception, psycopg2.Error) as error:
        print("Error while inserting user:", error)
        return None, error
    finally:
        connection.commit()

def read_user(connection, customer_id):
    '''
    read user method would be used when we need to rerun inference on a model
    '''
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE customer_id = %s", (customer_id,))
        user_data = cursor.fetchone()
        cursor.close()
        return user_data
    except (Exception, psycopg2.Error) as error:
        print("Error while reading users:", error)
        return None
    finally:
        connection.commit()

def update_user(connection, customer_id, updated_data):
    '''
    Default method to update user data in the 'users' table
    This may be used when we want to update the feature data of a user.
    '''
    try:
        cursor = connection.cursor()

        # Update user data in the 'user' table
        cursor.execute("""
            UPDATE users
            SET Credit_History_Age = %s,
                Monthly_Balance = %s,
                Annual_Income = %s,
                Changed_Credit_Limit = %s,
                Outstanding_Debt = %s
            WHERE customer_id = %s
        """, (*updated_data, customer_id))
        cursor.close()
    except (Exception, psycopg2.Error) as error:
        print("Error while updating user:", error)
    finally:
        connection.commit()

def update_credit_score(connection, customer_id, model_key, credit_score):
    '''
    When a new user credit score is evaluated we want to cache it to the credit score table.
    '''
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO creditscore
            VALUES (%s, %s, %s)
            ON CONFLICT (customer_id, model_key) DO UPDATE
            SET creditscore = EXCLUDED.creditscore
        """, (customer_id, model_key, credit_score))
        cursor.close()
    except (Exception, psycopg2.Error) as error:
        print("Error while updating credit score:", error)
    finally:
        connection.commit()

def fetch_credit_score(connection, customer_id, model_key):
    '''
    get credit score from cached table this is used when we want to evaluate the model
    '''
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT creditscore FROM creditscore WHERE customer_id = %s AND model_key = %s", (customer_id, model_key))   
        credit_score = cursor.fetchone()
        cursor.close()
        return credit_score[0] if credit_score else None
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching credit score:", error)
        return None
    finally:
        connection.commit()
