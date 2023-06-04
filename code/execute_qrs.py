import csv
from pathlib import Path

import pymssql

# server = 'mssqlserver'
user = 'sa'
password = 'MsSqlServer2022!'
database = 'master'
conn = pymssql.connect(server='localhost', user=user, password=password, database=database)
cursor = conn.cursor()


def query_to_csv(cursor, filename):
    filepath = Path(f'docs/{filename}')
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w') as f:
        outcsv = csv.writer(f)
        # write column titles
        outcsv.writerow(x[0] for x in cursor.description)
        # write query results
        outcsv.writerows(cursor.fetchall())


# Restore AdventureWorks2019
restore_db = """USE [master];IF DB_ID('AdventureWorks2019') IS NULL
RESTORE DATABASE [AdventureWorks2019]
FROM DISK = '/var/opt/mssql/backup/AdventureWorks2019.bak'
WITH
    MOVE 'AdventureWorks2019' TO '/var/opt/mssql/data/AdventureWorks2019.mdf',
    MOVE 'AdventureWorks2019_log' TO '/var/opt/mssql/data/AdventureWorks2019_log.ldf',
    FILE = 1,
    NOUNLOAD,
    STATS = 5"""

conn.autocommit(True)
cursor.execute(restore_db)

# Run queries
file_name_qr1 = 'ByJobTitle.csv'
stmt_by_job_title = """USE [AdventureWorks2019];SELECT * FROM HumanResources.Employee AS E
                       ORDER BY E.JobTitle"""
cursor.execute(stmt_by_job_title)
query_to_csv(cursor, file_name_qr1)

file_name_qr2 = 'ByLastName.csv'
stnt_employees_by_lastnaname = """USE [AdventureWorks2019];SELECT * FROM HumanResources.Employee AS E JOIN Person.Person
                                  AS P ON E.BusinessEntityID=P.BusinessEntityID ORDER BY LastName"""
cursor.execute(stnt_employees_by_lastnaname)
query_to_csv(cursor, file_name_qr2)

file_name_qr3 = 'Only3colByLastName.csv'
stmt_3_cols_by_last_name = """USE [AdventureWorks2019];SELECT P.FirstName, P.LastName, P.BusinessEntityID
                              AS Employee_id FROM Person.Person AS P ORDER BY P.LastName"""
cursor.execute(stmt_3_cols_by_last_name)
query_to_csv(cursor, file_name_qr3)

conn.autocommit(False)
cursor.close()
