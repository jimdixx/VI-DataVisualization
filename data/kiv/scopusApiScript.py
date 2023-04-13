import requests
import json
import textwrap
import csv
import time

MY_API_KEY = ""
OXFORD_DATA = "../OXFORD_DATA.csv"
MIT_DATA = "../MIT_DATA.csv"
OXFORD_DATA_FULL = "../OXFORD_DATA_FULL.csv"
MIT_DATA_FULL = "../MIT_DATA_FULL.csv"
KIV_DATA = "../KIV_DATA.csv"
KIV_DATA_FULL = "../KIV_DATA_FULL.csv"


def get_info_from_scopus_by_DOI(dokument_DOI):
    url = ("https://api.elsevier.com/content/search/scopus"
          + "?query="
          + dokument_DOI)

    resp = requests.get(url, headers={'Accept': 'application/json', 'X-ELS-APIKey': MY_API_KEY})

    return json.loads(resp.text.encode('utf-8'))


def get_number_of_institutes(link):
    resp = requests.get(link, headers={'Accept': 'application/json', 'X-ELS-APIKey': MY_API_KEY})
    data = json.loads(resp.text.encode('utf-8'))
    if data["abstracts-retrieval-response"].get("affiliation") is not None:
        if len(data["abstracts-retrieval-response"].get("affiliation")) == 5:
            if data["abstracts-retrieval-response"].get("affiliation").get("@id") is not None:
                return 1
        return len(json.loads(resp.text.encode('utf-8'))["abstracts-retrieval-response"]["affiliation"])
    return 1


def load_data(file_path):
    f = open(file_path, "r")
    reader = csv.reader(f)
    file = {}
    header = next(reader)[0].split(";")
    rows = []
    i = 0
    for row in reader:
        firstcol = row[0].split(";")
        row2 = []
        if len(firstcol[0]) > 1:
            dok = {}
            dok[header[0]] = firstcol[0]
            row2.append(firstcol[1])
            for a in row[1:len(row)]:
                row2.append(a)
            dok[header[1]] = row2
            dok["num_authors"] = len(row2)
            file[i] = dok
            i += 1
    f.close()
    print()
    return file


def save_data(pathFile, data):
    f = open(pathFile, "w")
    for keys in data[0]:
        out = "{};".format(keys)
        f.write(out)
    f.write("\n")
    for row in data.keys():
        for itemkey in data[row]:
            if itemkey == "coo_authors":
                for item in data[row][itemkey]:
                    f.write("{},".format(item))
                f.write(";")
            else:
                out = "{};".format(data[row][itemkey])
                f.write(out)
        f.write("\n")
    f.close()


csv_file = load_data(KIV_DATA)

i = 0
result = {}
for row in csv_file.values():
    d = get_info_from_scopus_by_DOI(row["doi"])
    if d.get("search-results") is not None:
        dokument = d["search-results"]["entry"][0]
        if dokument.get("error") is None:
            row["num_citation"] = dokument["citedby-count"]
            dok = get_number_of_institutes(dokument["link"][1]["@href"])
            row["num_institution"] = dok
            row["date"] = dokument["prism:coverDate"]
            print(row)
            result[i] = row
            i += 1
    time.sleep(0.5)

save_data(KIV_DATA_FULL, result)