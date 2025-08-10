import json
import glob
from pprint import pprint

entries = []
for path in glob.glob("results/*.json"):
    with open(path, "r") as file:
        entries.append(json.load(file))

costs = [(entry["repo"], entry["rebuildCost"]) for entry in entries]
costs.sort(key=lambda x: x[1])

pprint(costs)
