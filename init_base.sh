#!/bin/bash

sleep 30

/opt/mssql-tools/bin/sqlcmd -S 172.17.0.1 -U sa -P "MsSqlServer2022!" -d master -i /tmp/recreate_db.sql
