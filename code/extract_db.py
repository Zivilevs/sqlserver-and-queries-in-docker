import requests
from pathlib import Path

remote_url = 'https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorks2019.bak'
data = requests.get(remote_url)

filepath = Path('code/docs/AdventureWorks2019.bak')
filepath.parent.mkdir(parents=True, exist_ok=True)

with filepath.open('wb') as f:
    f.write(data.content)

if filepath.exists:
    print(f'{filepath.name} received.')
