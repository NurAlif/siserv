CREATE USER oftg WITH PASSWORD 'secure_password';
CREATE DATABASE lingojourn_db;
GRANT CONNECT ON DATABASE lingojourn_db TO oftg;
GRANT ALL PRIVILEGES ON DATABASE lingojourn_db TO oftg;