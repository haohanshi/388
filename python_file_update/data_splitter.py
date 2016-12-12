import json

# data_splitter splits the collected data to two parts for cross-validation
# the first part contains of 70% of the data and the second part contains 30%
# the 70% part is for training the svm
# the 30% part is reserved for cross validation

# this list is for 
pages = []

# dump 70% of the data into the "<page name>_70" file
for page in pages:
    with open("{}.json".format(page), "r") as f:
        s = json.load(f)
        # the data set collected from college confidential website is in a
        # different format from the data set collected from facebook pages
        if (page == 'college.confidential'):
            flattend = s
        else:
            flattend = [item for sublist in s for item in sublist]
        length = int(0.7*len(flattend))
        print("writing 70 percent of {}...".format(page))
        with open("{}_70.json".format(page), 'w') as wf:
            json.dump(flattend[:length], wf)

# dump 30% of the data into the "<page name>_30" file
for page in pages:
    with open("{}.json".format(page), "r") as f:
        s = json.load(f)
        # the data set collected from college confidential website is in a
        # different format from the data set collected from facebook pages
        if (page == 'college.confidential'):
            flattend = s
        else:
            flattend = [item for sublist in s for item in sublist]
        length = int(0.7*len(flattend))
        print("writing 30 percent of {}...".format(page))
        with open("{}_30.json".format(page), 'w') as wf:
            json.dump(flattend[length:], wf)
