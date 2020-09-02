import json

import requests
import pandas as pd
df = pd.read_csv(r'../upload/auth-users-2020-9-2.csv')
res = df.to_json(orient='records')
res = json.loads(res)
for r in res:
    print(r)
res = requests.post('https://acme.com/api/v1/authorized-users?', json={})
print(res)