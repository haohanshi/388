# this file removes repetitions from the collected data

import json

pages = []

def remove_rep(l):
    unique = set()
    for text in l:
        unique.add(text)
    return list(unique)

for page in pages:
    with open("{}.json".format(page), "r") as f:
        s = json.load(f)
        if (page == 'college.confidential'):
            flattend = s
        else:
            flattend = [item for sublist in s for item in sublist]
        unique = remove_rep(flattend)
        print("removing dups for {}...".format(page))
        with open("{}_unique.json".format(page), 'w') as wf:
            json.dump(unique, wf)
