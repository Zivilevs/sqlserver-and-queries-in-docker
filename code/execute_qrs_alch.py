import csv
import os
from pathlib import Path

import sqlalchemy as sa
from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import URL

load_dotenv()


def HandleHierarchyId(value):
    return str(value)


def query_to_csv(data, filename):
    filepath = Path(f'docs/{filename}')
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w') as f:
        outcsv = csv.writer(f)
        # write column titles
        outcsv.writerow(data.keys())
        # write query results
        outcsv.writerows(data.fetchall())


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

metadata = MetaData()
hr = sa.Table('Employee', metadata, schema='HumanResources', autoload_with=engine)
person = sa.Table('Person', metadata, schema='Person', autoload_with=engine)

# query 1
stmt = sa.select(hr).order_by(hr.c.JobTitle)
result = conn.execute(stmt)
query_to_csv(result, 'ByJobTitle1.csv')

# quesry 2
joined = sa.join(hr, person, hr.c.BusinessEntityID == person.c.BusinessEntityID)
stmt2 = sa.select(joined).select_from(joined).order_by(person.c.LastName)
result = conn.execute(stmt2)
query_to_csv(result, 'ByLastName1.csv')

# qurey 3
stmt3 = sa.select(person.c.FirstName, person.c.LastName,
                  person.c.BusinessEntityID.label('Employee_id')).order_by(person.c.LastName)
result = conn.execute(stmt3)
query_to_csv(result, 'Only3colByLastName1.csv')
