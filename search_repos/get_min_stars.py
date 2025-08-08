import json
import glob

min_star = 1e9

d = dict()

for path in sorted(glob.glob("repos/*.json")):
    with open(path, 'r') as f:
        data = json.load(f)
        stars = data['stargazers_count']
        if stars < min_star:
            min_star = stars
        if stars in d:
            d[stars] += 1
        else:
            d[stars] = 1

print(min_star)

for k in sorted(d.keys()):
    print(k, d[k])
