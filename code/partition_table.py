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

'''
-- Create a partition function
CREATE PARTITION FUNCTION PFshort_ProductID(integer)
AS RANGE LEFT FOR VALUES (1, 100, 200, 300, 400, 500,
						  600, 700, 800, 900, 1000);

-- Create a partition scheme

CREATE PARTITION SCHEME PS3_productID 
AS PARTITION PFshort_ProductID  
ALL TO ('PRIMARY');

-- Create a new partitioned table

USE AdventureWorks2019;

CREATE TABLE Production.TransactionHistoryPartitioned(
	TransactionID int IDENTITY(100000,1) NOT NULL,
	ProductID int NOT NULL,
	ReferenceOrderID int NOT NULL,
	ReferenceOrderLineID int DEFAULT 0 NOT NULL,
	TransactionDate datetime DEFAULT getdate() NOT NULL,
	TransactionType nchar(1) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	Quantity int NOT NULL,
	ActualCost money NOT NULL,
	ModifiedDate datetime DEFAULT getdate() NOT NULL,
	CONSTRAINT PK_TransactionHistory_TransactionID PRIMARY KEY (TransactionID),
	CONSTRAINT FK_TransactionHistory_Product_ProductID FOREIGN KEY (ProductID) REFERENCES Production.Product(ProductID))
ON PS3_productID (ProductID);


----- SQL Error [1921] [S0001]: Invalid partition scheme 'PS3_productID' specified.-----
select * from sys.partition_schemes;


CREATE NONCLUSTERED INDEX IX_TransactionHistory_ProductID ON AdventureWorks2019.Production.TransactionHistory (ProductID);
CREATE NONCLUSTERED INDEX IX_TransactionHistory_ReferenceOrderID_ReferenceOrderLineID ON AdventureWorks2019.Production.TransactionHistory (ReferenceOrderID, ReferenceOrderLineID);
ALTER TABLE AdventureWorks2019.Production.TransactionHistory WITH NOCHECK ADD CONSTRAINT CK_TransactionHistory1_TransactionType
	CHECK (upper([TransactionType])='P' OR upper([TransactionType])='S' OR upper([TransactionType])='W');

 -- Copy data from the existing table to the new partitioned table
INSERT INTO AdventureWorks2019.Production.TransactionHistoryPartitioned (ProductID, ReferenceOrderID, ReferenceOrderLineID, TransactionDate, TransactionType, Quantity, ActualCost, ModifiedDate)
SELECT ProductID, ReferenceOrderID, ReferenceOrderLineID, TransactionDate, TransactionType, Quantity, ActualCost, ModifiedDate
FROM AdventureWorks2019.Production.TransactionHistory;
'''
