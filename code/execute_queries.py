import pymssql
import csv

from pathlib import Path


server = 'mssqlserver'
user = 'sa'
password = 'MsSqlServer2022!'
database = 'master'
conn = pymssql.connect(server=server, user=user, password=password, database=database)
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


# restore AdventureWorks2019
query0 = """USE [master];IF DB_ID('AdventureWorks2019') IS NULL
RESTORE DATABASE [AdventureWorks2019]
FROM DISK = '/var/opt/mssql/backup/AdventureWorks2019.bak'
WITH
    MOVE 'AdventureWorks2019' TO '/var/opt/mssql/data/AdventureWorks2019.mdf',
    MOVE 'AdventureWorks2019_log' TO '/var/opt/mssql/data/AdventureWorks2019_log.ldf',
    FILE = 1,
    NOUNLOAD,
    STATS = 5"""

conn.autocommit(True)
cursor.execute(query0)


file1 = 'ByJobTitle.csv'
query1 = """USE [AdventureWorks2019];SELECT * FROM HumanResources.Employee AS E
            ORDER BY E.JobTitle"""
cursor.execute(query1)
query_to_csv(cursor, file1)

file2 = 'ByLastName.csv'
query2 = """USE [AdventureWorks2019];SELECT * FROM HumanResources.Employee AS E JOIN Person.Person
            AS P ON E.BusinessEntityID=P.BusinessEntityID ORDER BY LastName"""
cursor.execute(query2)
query_to_csv(cursor, file2)

file3 = 'Only3colByLastName.csv'
query3 = """USE [AdventureWorks2019];SELECT P.FirstName, P.LastName, P.BusinessEntityID
            AS Employee_id FROM Person.Person AS P ORDER BY P.LastName"""
cursor.execute(query3)
query_to_csv(cursor, file3)

conn.autocommit(False)
cursor.close()
