#!/bin/bash

sleep 70

/opt/mssql-tools/bin/sqlcmd -S mssqlserver -U sa -P "MsSqlServer2022!" -d master -i /tmp/recreate_db.sql
