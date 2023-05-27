import requests
from pathlib import Path


filepath = Path('docs/AdventureWorks2019.bak')
filepath.parent.mkdir(parents=True, exist_ok=True)

if not filepath.is_file():
    remote_url = 'https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorks2019.bak'
    data = requests.get(remote_url)

    with open(filepath, 'wb') as file:
        file.write(data.content)
else:
    print(f'{filepath.name} received.')
