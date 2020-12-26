import json, re
from bs4 import BeautifulSoup as bs
import csv


probs = []
with open("scraper-out.txt", "r") as f:
    for each in f:
        obj = json.loads(each)
        obj["statement"] = bs(obj["statement"], "lxml").text
        obj["statement"] = re.sub(r'\$\$\$', '', obj["statement"])
        obj["title"] = obj["title"][3:]
        probs.append(obj)

m = {}
with open("api-out.csv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    i = 0
    keys = []
    for ln in reader:
        if i == 0:
            keys = ln
        else:
            temp = {}
            for i in range(len(keys)):
                temp[keys[i]] = ln[i]

            if ln[0] in m.keys():
                m[ln[0]][ln[1]] = temp
            else:
                m[ln[0]] = {ln[1]: temp}
        i += 1


for each in probs:
    k1 = each["contest_id"]
    k2 = each["in_contest_id"]
    meta = m[k1][k2]
    for (k, v) in meta.items():
        each[k] = v

with open("preprocessed.tsv", "w+") as f:
    keys = list(probs[0].keys())
    for i in range(len(keys)):
        f.write(keys[i])
        if (i < len(keys) - 1):
            f.write("\t\t\t")
        else:
            f.write("\n")


    for each in probs:
        values= list(each.values())
        for i in range(len(values)):
            f.write(values[i].__str__())
            if (i < len(values) - 1):
                f.write("\t\t\t")
            else:
                f.write("\n")
            

        