import requests
import json

url = "https://students.kiv.zcu.cz/~urbanp/bcproject/index.php?ws=dblp_get_pids"

response = requests.get(url)
data = json.loads(response.text)

orion_logins = [d['orion'] for d in data if d['dblp_pid'] != 'none']

with open('orion_logins.txt', 'w') as f:
    for orion in orion_logins:
        f.write(orion + '\n')

