import pyodbc
import os

from dotenv import load_dotenv


load_dotenv()

server = os.environ.get('ms_server')
username = os.environ.get('ms_user')
password = os.environ.get('ms_sa_password')
database = os.environ.get('ms_default_database')


conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'
                      f'SERVER=localhost,1433;'
                      f'DATABASE={database};'
                      f'Encrypt=no;'
                      f'UID={username};'
                      f'PWD={password};')

conn.autocommit = True
cursor = conn.cursor()
test = """USE [AdventureWorks2019];select count(*) from Person.person"""
cursor.execute(test)
while cursor.nextset():
    print(cursor.fetchall())
cursor.close()
