import os
import time
import json
import glob
from tqdm import tqdm

from github import Github, Auth


def get_token():
    with open(os.path.join(os.path.dirname(__file__), "..", "token.txt"), "r") as f:
        return f.read().strip()


AUTH = Auth.Token(get_token())
GH = Github(auth=AUTH)

os.makedirs("trees", exist_ok=True)

jsons = list(glob.glob("repos/*.json"))
jsons = [json_path for json_path in jsons if not os.path.exists(f"trees/{os.path.basename(json_path).replace('.json', '_tree.json')}")]
jsons.sort()

pbar = tqdm(jsons)
for i, json_path in enumerate(pbar):
    pbar.set_postfix({"repo": os.path.basename(json_path)})
    with open(json_path, 'r') as f:
        pbar.set_description("Processing")

        data = json.load(f)
        default_branch = data["default_branch"]
        repo_name = data["full_name"]
        result_file_path = f"trees/{repo_name.replace('/', '__')}_tree.json"

        try:
            pbar.set_description("Fetching")
            tree = GH.get_repo(repo_name).get_git_tree(sha=default_branch, recursive=False)
            pbar.set_description("Fetched")
            tree_data = [item._rawData for item in tree.tree]

            with open(result_file_path, 'w') as tree_file:
                json.dump(tree_data, tree_file, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error processing {repo_name}: {e}")