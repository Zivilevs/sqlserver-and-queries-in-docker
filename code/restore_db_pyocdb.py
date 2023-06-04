import os

import pyodbc
from dotenv import load_dotenv

load_dotenv()

server = os.environ.get('ms_server')
username = os.environ.get('ms_user')
password = os.environ.get('ms_sa_password')
database = os.environ.get('ms_default_database')


conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'
                      'SERVER=localhost,1433;'
                      f'DATABASE={database};'
                      'Encrypt=no;'
                      f'UID={username};'
                      f'PWD={password};')


conn.autocommit = True
cursor = conn.cursor()

restore = """USE [master];IF DB_ID('AdventureWorks2019') IS NULL
RESTORE DATABASE [AdventureWorks2019]
FROM DISK = '/var/opt/mssql/backup/AdventureWorks2019.bak'
WITH
    MOVE 'AdventureWorks2019' TO '/var/opt/mssql/data/AdventureWorks2019.mdf',
    MOVE 'AdventureWorks2019_log' TO '/var/opt/mssql/data/AdventureWorks2019_log.ldf',
    FILE = 1,
    NOUNLOAD,
    STATS = 5"""
res = cursor.execute(restore)
cursor.close()
