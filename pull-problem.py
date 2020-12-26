import csv
import requests as api
import json
import time
from math import floor


problems = {}

with open("api-out.csv", "r") as f:
    df = csv.reader(f, delimiter="\t") 
    i = 0
    for each in df:
        i+=1
        if i == 1: continue 
        if each[0] in problems:
            problems[each[0]].add(each[1])
        else:
            problems[each[0]] = set({each[1]})


cnt = 0
start_time = time.time()
with open("scraper-out.txt", "w") as f:
    for (k, v) in problems.items():
        # send request to the flask server
        # https://github.com/kerolloz/codeforces-problem-scraper-api
        for each in v:
            req = f"http://localhost:5000/?id={k}/problem/{each}"
            
            attempts = 0
            while attempts < 2:
                try:
                    res = api.get(req)
                    res = res.json()
                    break
                except:
                    attempts += 1
            
            if attempts == 2: continue

            res["contest_id"] = k
            res["in_contest_id"] = each
            f.write(json.dumps(res))
            f.write("\n")
            cnt+=1
            if (cnt % 10 == 0):
                print(f"--{floor(time.time() - start_time+ 0.5)} seconds have elapsed--", end=": ")
                print(cnt)
        f.flush()
