import requests
from pathlib import Path


remote_url = 'https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorks2019.bak'

dir_path = Path().absolute()
local_file = f'{dir_path}/AdventureWorks2019.bak'


data = requests.get(remote_url)

with open(local_file, 'wb') as file:
    file.write(data.content)

print(f'{local_file} received.')