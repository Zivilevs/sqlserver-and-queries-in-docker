# AdventureWorks MS SQL server database set up and query in Docker

A set up using docker services to extract and query [AdventureWorks database](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver16&tabs=tsql) provided for learning purpose by Microsoft.
1. First service extracts and downloads database backup file.
2. Second service sets up MS SQL Server in docker container and loads the backup file.
3. Third service makes a connection to SQL Server using `pymssql` library. It restores a database and queries 3 example writing them out to csv files for inspection.



Requirements:
[Docker and docker compose](https://docs.docker.com/compose/install/)

Once repo is cloned:
```docker-compose up --build```


