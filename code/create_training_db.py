# Create new "Training" database and users
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()


username = os.environ.get('MS_USER')
password = os.environ.get('MS_SA_PASSWORD')
training_password = os.environ.get('TRAINING_PASSWORD')
database = os.environ.get('MS_DEFAULT_DATABASE')

connection_string = ('DRIVER={ODBC Driver 18 for SQL Server};'
                     'SERVER=localhost,1433;'
                     f'DATABASE={database};'
                     'Encrypt=no;'
                     f'UID={username};'
                     f'PWD={password};')

connection_url = URL.create('mssql+pyodbc',
                            query={'odbc_connect': connection_string})

engine = create_engine(connection_url, connect_args={'autocommit': True})
conn = engine.connect()

conn.execute(text("IF DB_ID('Training') IS NULL CREATE DATABASE Training;"))
res = conn.execute(text('SELECT name FROM sys.databases;'))

print('Databases on server:')
for row in res:
    print(row)

# Create users

create_user = f"""USE training;
IF NOT EXISTS(SELECT name from training.sys.server_principals WHERE name='training')
BEGIN
CREATE LOGIN training WITH PASSWORD='{training_password}';
USE Training;
CREATE USER training FOR LOGIN training;
ALTER ROLE db_datareader ADD MEMBER training;
ALTER ROLE db_datawriter ADD MEMBER training;
END"""
conn.execute(text(create_user))

show_users = """select name from training.sys.server_principals where type_desc='SQL_LOGIN';"""
res = conn.execute(text(show_users))

print('Database logins:')
for row in res:
    print(row)
