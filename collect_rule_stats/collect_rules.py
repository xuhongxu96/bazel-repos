import os
import re
import json
import glob

RE_RULE = re.compile(r'rule class="([a-zA-Z_0-9]*?)"')

RES_DIR = "results"

os.makedirs(RES_DIR, exist_ok=True)

for path in sorted(glob.glob("../get_rebuild_costs/results/*-query.xml")):
    print(path)
    rule_counts = dict()
    with open(path, "r") as f:
        data = f.read()
        for match in RE_RULE.finditer(data):
            rule = match.group(1)
            if rule not in rule_counts:
                rule_counts[rule] = 0
            rule_counts[rule] += 1
    # Save rule counts into result dir in desc order
    rule_counts = sorted(rule_counts.items(), key=lambda x: x[1], reverse=True)
    with open(os.path.join(RES_DIR, os.path.basename(path).replace("-query.xml", "-rule-stats.json")), "w") as f:
        json.dump(rule_counts, f, indent=2)
    print(rule_counts)