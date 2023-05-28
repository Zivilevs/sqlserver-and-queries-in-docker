USE master
IF NOT EXISTS(
    SELECT name from master.sys.server_principals WHERE name='reporting'
)
BEGIN
CREATE LOGIN reporting WITH PASSWORD='Reporting123'
USE AdventureWorks2019
CREATE USER reporting FOR LOGIN reporting
ALTER ROLE db_datareader ADD MEMBER reporting
ALTER ROLE db_datawriter ADD MEMBER reporting
END
                                                