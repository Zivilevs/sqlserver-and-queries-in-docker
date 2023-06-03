import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()


def HandleHierarchyId(value):
    return str(value)


username = os.environ.get('ms_user')
password = os.environ.get('ms_sa_password')
database = os.environ.get('ms_default_database')

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

stmt = """SELECT top 5 m.name as schema_name, t.name AS table_name, s.row_count AS row_count
FROM   sys.tables t
JOIN   sys.dm_db_partition_stats s
  ON t.object_id  = s.object_id
JOIN sys.schemas m
ON m.schema_id=t.schema_id
 AND t.type_desc = 'USER_TABLE'
 AND s.index_id IN (0, 1)
ORDER  BY row_count desc;"""

res = conn.execute(text(stmt))

print(res.keys())
for row in res.fetchall():
    print(row)

conn.close()
