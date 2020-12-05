import requests as api
import json
from time import sleep

tags = ["expression parsing","fft","two pointers",
    "binary search","dsu","strings","number theory",
    "data structures","hashing","shortest paths",
    "matrices","string suffix structures",
    "graph matchings","dp","dfs and similar",
    "meet-in-the-middle","games","schedules",
    "constructive algorithms","greedy","bitmasks",
    "divide and conquer","flows","geometry","math",
    "sortings","ternary search","combinatorics",
    "brute force","implementation","2-sat","trees",
    "probabilities","graphs","chinese remainder theorem"]

# https://codeforces.com/api/{methodName}
host = "https://codeforces.com/api/"

class Problem:
    def __init__(self, obj):
        self.contest_id = obj["contestId"]
        self.in_contest_id = obj["index"]
        self.name = obj["name"]
        self.type = obj["type"]
        self.points = obj["points"] if "points" in obj else -1
        self.rating = obj["rating"] if "rating" in obj else -1
        self.tags = obj["tags"]
    
    def _tags_to_str(self):
        res = ""
        for each in self.tags:
            res += each
            res += "/"
        return res[:-1]

    def to_csv(self):
        return f"{self.contest_id}\t{self.in_contest_id}\t{self.name}\t{self.type}\t{self.points}\t{self.rating}\t{self._tags_to_str()}"

problems = []

def main():
    for tag in tags:
        res = api.get(f"{host}problemset.problems?tags={tag}")
        res = res.json()
        res = res["result"]["problems"]
        for each in res:
            problems.append(Problem(each))
        
        with open("api-out.csv", "w+") as f:
            f.write("contest_id\tin_contest_id\tname\ttype\tpoints\trating\ttags\n")
            for each in problems:
                f.write(each.to_csv())
                f.write("\n")
            print(f"finished writing {len(problems)} to file api-out.csv")
        sleep(0.5)


if __name__ == "__main__":
    main()
