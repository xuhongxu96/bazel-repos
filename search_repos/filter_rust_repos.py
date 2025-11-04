import os
import shutil
import json
import glob

os.makedirs("filtered_rust", exist_ok=True)

jsons = sorted(glob.glob("trees/*.json"))


def is_rust_related_files(path: str):
    return path in ["Cargo.toml"]


i = 0
star_list = []
for json_path in jsons:
    with open(json_path, "r") as f:
        data = json.load(f)

        blobs = [
            item
            for item in data
            if item["type"] == "blob" and is_rust_related_files(item["path"])
        ]
        if blobs:
            json_name = os.path.basename(json_path).replace("_tree.json", ".json")
            with open(f"repos/{json_name}", "r") as repo_file:
                repo_data = json.load(repo_file)
                repo_name = repo_data["full_name"]
                star_count = repo_data["stargazers_count"]

            star_list.append((star_count, repo_name))

            i += 1
            print(f"Filtered rust-related files for {repo_name} saved successfully.")

print(f"{i}/{len(jsons)} repositories have rust-related files.")

star_list.sort(key=lambda x: x[0], reverse=True)

with open("rust_repo_stars.json", "w") as f:
    json.dump(star_list, f, indent=2)
