import os
import time
import math
import json
import glob

from pprint import pprint
from github import Github, Auth


def get_token():
    with open(os.path.join(os.path.dirname(__file__), "..", "token.txt"), "r") as f:
        return f.read().strip()


AUTH = Auth.Token(get_token())
GH = Github(auth=AUTH)

os.makedirs("repos", exist_ok=True)

end_star = 64

while end_star > 1:
    print(f"Searching for repositories with stars less than {end_star}...")

    search = GH.search_repositories(f"size:>1000 pushed:>2025-01-01 stars:<={end_star} fork:false archived:false template:false mirror:false", sort="stars", order="desc")
    print(search.totalCount)

    for i in range(math.ceil(search.totalCount / search._PaginatedList__requester.per_page)):
        time.sleep(1)
        code = search.get_page(i)
        for item in code:
            raw_data = item._rawData
            repo_name = raw_data["full_name"]
            end_star = raw_data["stargazers_count"]

            print(f"Processing {repo_name} with {end_star} stars...")

            with open(f"repos/{repo_name.replace('/', '__')}.json", 'w') as repo_file:
                json.dump(raw_data, repo_file, indent=2, ensure_ascii=False)
