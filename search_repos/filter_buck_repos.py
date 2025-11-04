import os
import shutil
import json
import glob

os.makedirs("filtered_buck", exist_ok=True)

jsons = sorted(glob.glob("trees/*.json"))


def is_buck_related_files(path: str):
    return path in ["BUCK"]


i = 0
for json_path in jsons:
    with open(json_path, "r") as f:
        data = json.load(f)

        blobs = [
            item
            for item in data
            if item["type"] == "blob" and is_buck_related_files(item["path"])
        ]
        if blobs:
            json_name = os.path.basename(json_path).replace("_tree.json", ".json")
            with open(f"repos/{json_name}", "r") as repo_file:
                repo_data = json.load(repo_file)
                repo_name = repo_data["full_name"]

            shutil.copyfile(f"repos/{json_name}", f"filtered_buck/{json_name}")

            i += 1
            print(f"Filtered buck-related files for {repo_name} saved successfully.")

print(f"{i}/{len(jsons)} repositories have buck-related files.")
