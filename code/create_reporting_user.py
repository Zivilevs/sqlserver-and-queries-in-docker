import os

import pyodbc
from dotenv import load_dotenv

load_dotenv()

server = os.environ.get('MS_SERVER')
username = os.environ.get('MS_USER')
password = os.environ.get('MS_SA_PASSWORD')
database = os.environ.get('MS_DEFAULT_DATABASE')


conn1 = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'
                       'SERVER=localhost,1433;'
                       f'DATABASE={database};'
                       'Encrypt=no;'
                       f'UID={username};'
                       f'PWD={password};')


conn1.autocommit = True
cursor = conn1.cursor()

restore = """USE master;
IF NOT EXISTS(SELECT name from master.sys.server_principals WHERE name='reporting')
BEGIN
CREATE LOGIN reporting WITH PASSWORD='Reporting123';
USE AdventureWorks2019;
CREATE USER reporting FOR LOGIN reporting;
ALTER ROLE db_datareader ADD MEMBER reporting;
ALTER ROLE db_datawriter ADD MEMBER reporting;
END"""
res = cursor.execute(restore)
cursor.close()


conn2 = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'
                       'SERVER=localhost,1433;'
                       'DATABASE=master;'
                       'Encrypt=no;'
                       'UID=reporting;'
                       'PWD=Reporting123;')

cursor = conn2.cursor()

check1 = """SELECT * FROM fn_my_permissions(NULL, 'Database')"""
res = cursor.execute(check1)

print('User reporting permissions on master')
for row in res.fetchall():
    print(row)

cursor.close()


conn3 = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'
                       'SERVER=localhost,1433;'
                       'DATABASE=AdventureWorks2019;'
                       'Encrypt=no;'
                       'UID=reporting;'
                       'PWD=Reporting123;')

cursor = conn3.cursor()

check2 = """SELECT * FROM fn_my_permissions(NULL, 'Database')
    ORDER BY subentity_name, permission_name;"""
res = cursor.execute(check2)

print('User reporting permissions on AdventureWorks2019')
for row in res.fetchall():
    print(row)
cursor.close()
