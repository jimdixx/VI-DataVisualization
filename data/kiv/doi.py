import requests
import time
import json

url_template = "http://students.kiv.zcu.cz/~urbanp/bcproject/index.php?ws=dblp_publications&name={}&year={}"

year_range = range(1990, 2024)

with open('orion_logins.txt', 'r') as f:
    names = f.read().splitlines()

names_and_dois = {}

# Iterate over each orion login
for name in names:
    dois = []
    # Iterate over each year
    for year in year_range:
        # Format the URL with the current orion and year values
        current_url = url_template.format(name, year)

        response = requests.get(current_url)

        print(current_url, response.status_code)

        data = json.loads(response.text)

        for item in data:
            if 'doi' in item:
                dois.append(item['doi'])

        # Pause for 0.5 sec
        time.sleep(0.5)

    names_and_dois[name] = dois

# convert the hashmap to a JSON string
json_string = json.dumps(names_and_dois)

with open('output.json', 'w') as f:
    json.dump(names_and_dois, f)

