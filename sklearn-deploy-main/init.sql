SET log_statement = 'all';
CREATE DATABASE default_database;
\connect default_database;

-- Create the 'users' table
CREATE TABLE users (
    customer_id VARCHAR(50) PRIMARY KEY,
    Credit_History_Age FLOAT,
    Monthly_Balance FLOAT,
    Annual_Income FLOAT,
    Changed_Credit_Limit FLOAT,
    Outstanding_Debt FLOAT
);

-- Create the 'creditscore' table with foreign key constraint
CREATE TABLE creditscore (
    customer_id VARCHAR(50) REFERENCES users(customer_id),
    model_key VARCHAR(50),
    creditscore VARCHAR(10),
    PRIMARY KEY (customer_id, model_key)
);

CREATE USER apiuser WITH ENCRYPTED PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE default_database TO apiuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO apiuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO apiuser;