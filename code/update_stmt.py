import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()


def HandleHierarchyId(value):
    return str(value)


username = os.environ.get('MS_USER')
password = os.environ.get('MS_SA_PASSWORD')
database = os.environ.get('MS_DEFAULT_DATABASE')

connection_string = ('DRIVER={ODBC Driver 18 for SQL Server};'
                     'SERVER=localhost,1433;'
                     f'DATABASE={database};'
                     'Encrypt=no;'
                     f'UID={username};'
                     f'PWD={password};')

connection_url = URL.create(
    'mssql+pyodbc',
    query={'odbc_connect': connection_string}
    )

engine = create_engine(connection_url)

conn = engine.connect()
conn.connection.add_output_converter(-151, HandleHierarchyId)

select_stmt = """SELECT P.FirstName, P.LastName, P.BusinessEntityID AS Employee_id
                 FROM Person.Person AS P
                 WHERE P.LastName = 'Silveira' OR P.LastName = 'Abel'
                 """
update_lastname = """UPDATE Person.Person
                     SET LastName='Silveira' where LastName = 'Abel' and BusinessEntityID = '293'
                     """
# Before update
res = conn.execute(text(select_stmt))

print(res.keys())
for row in res.fetchall():
    print(row)

# Update lastname
i = 0
while i in range(5):
    conn.execute(text(update_lastname))
    i += 1

# After update
res = conn.execute(text(select_stmt))

print(res.keys())
for row in res.fetchall():
    print(row)

conn.close()
