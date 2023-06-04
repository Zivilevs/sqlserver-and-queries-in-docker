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

drop_table = """DROP TABLE IF EXISTS #top_5;"""
temp_table = """SELECT top 5 m.name as schema_name, t.name AS table_name,
                s.row_count AS row_count, t.object_id as object_id
                INTO #top_5
                FROM   sys.tables t
                JOIN   sys.dm_db_partition_stats s
                  ON t.object_id  = s.object_id
                JOIN sys.schemas m
                ON m.schema_id=t.schema_id
                 AND t.type_desc = 'USER_TABLE'
                 AND s.index_id IN (0, 1)
                ORDER  BY row_count desc;
                """
find_top_tables_and_indexes = """SELECT t.*, f.name as foreign_key, i.name as index_name, i.type as index_type
                                 FROM #top_5 as t
                                 LEFT JOIN sys.foreign_keys f
                                 ON f.parent_object_id = t.object_id
                                 LEFT JOIN sys.indexes i
                                 ON i.object_id = t.object_id AND i.index_id NOT IN (0, 1)
                                 ;
                                 """
conn.execute(text(drop_table))
conn.execute(text(temp_table))
res = conn.execute(text(find_top_tables_and_indexes))

print(res.keys())
for row in res.fetchall():
    print(row)

conn.close()
