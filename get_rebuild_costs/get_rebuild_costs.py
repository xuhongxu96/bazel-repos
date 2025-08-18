import os
import glob
import json
import subprocess as sp
from pprint import pprint

DEPSTAT = "../../../depreduce/target/release/depstat"
QUERY = 'query deps(//...) --keep_going --notool_deps --noimplicit_deps --output xml'
paths = sorted(glob.glob("../search_repos/filtered/*.json"))

repos = []
for path in paths:
    with open(path, "r") as f:
        data = json.loads(f.read())
        if data:
            repos.append((data['stargazers_count'], data['full_name'], data['clone_url']))

repos = sorted(repos, key=lambda x: x[0], reverse=True)

for repo in repos:
    try:
        stars, name, clone_url = repo
        print(f"{stars} {name}")
        repo_path = f"../cloned_repos/{name.replace('/', '__')}"

        if os.path.exists(repo_path):
            print(f"Repository {name} already cloned.")
        else:
            os.system(f"git clone {clone_url} {repo_path}")

        result_path = f"results/{name.replace('/', '__')}.json"
        if os.path.exists(result_path):
            print(f"Results for {name} already exist, skipping.")
        else:
            p = sp.run([DEPSTAT, "-w", ".", "--deps-only"], cwd=repo_path, stdout=sp.PIPE, stderr=sp.PIPE)
            stdout = p.stdout.decode("utf-8")
            with open(f"results/{name.replace('/', '__')}.stdout", "w") as f:
                f.write(stdout)
            with open(f"results/{name.replace('/', '__')}.stderr", "w") as f:
                f.write(p.stderr.decode("utf-8"))

            rcost = (int(stdout.split("Rebuild cost: ")[1].strip()))
            print(rcost)

            with open(result_path, "w") as f:
                json.dump({"repo": name, "rebuildCost": rcost}, f, indent=2)

        result_path = f"results/{name.replace('/', '__')}-query.xml"
        if os.path.exists(result_path):
            print(f"Query results for {name} already exist, skipping.")
        else:
            p = sp.run(["bazel"] + QUERY.split(), cwd=repo_path, stdout=sp.PIPE, stderr=sp.PIPE)
            stdout = p.stdout.decode("utf-8")
            with open(result_path, "w") as f:
                f.write(stdout)
            with open(f"results/{name.replace('/', '__')}-query.stderr", "w") as f:
                f.write(p.stderr.decode("utf-8"))
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"Error processing {name}: {e}")
        with open(f"results/{name.replace('/', '__')}.error", "w") as f:
            f.write(str(e))
            f.flush()