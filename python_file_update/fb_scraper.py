# This file is the tool for scraping comments from public facebook pages.
# The facebook graph api is used for getting access to the comments from
# public pages.

import requests
import json
import pandas
import time
from time import sleep

# access token for facebook graph api
app_id = "1786012341650556"
app_secret = "deaada8ad48ddb190897068758c4d0ae"
access_token = app_id + "|" + app_secret

####################### helper functions #######################

def getid(pagename):
    url = "https://graph.facebook.com/" + 
           pagename + 
          "?access_token=" + 
           access_token
    text = str(requests.get(url).text)
    index = text.find('id":"')
    truncated_id = text[index + 5 : -2]
    return truncated_id

def getpost(pagename):
    msg = []
    id_list = []
    page_id = getid(pagename)

    url = "https://graph.facebook.com/v2.8/" + 
           page_id + 
          "/posts/?fields=message&limit=100&access_token=" + 
           access_token

    text = requests.get(url).text
    data = json.loads(text, strict=False)

    for set in data["data"]:
        if "message" in set:
            msg.append(set["message"])
        if "id" in set:
            id_list.append(set["id"])

    return msg, id_list
################################################################


# main function for getting comments from the given page
def getcomments(pagename):
    id_list = getpost(pagename)[1]

    raw = [] # comments in dict format
    parsed = [] # comments parsed to text only format

    num_comments = 0
    while num_comments < 10:
        for page_id in id_list:

            url = "https://graph.facebook.com/v2.8/" + 
                   page_id + 
                  "/comments?access_token=" + 
                   access_token

            response = (requests.get(url).text)
            raw_comments = {}
            parsed_comments = []

            try:
                raw_comments = json.loads(response, strict=False)["data"]
            except:
                continue

            for comment in raw_comments:
                try:
                    comment = comment["message"].encode("ascii")
                    comment = comment.decode("ascii")

                    # get sentences with more than 5 words
                    if (len(comment.split(" ")) > 5):
                        num_comments += 1
                        parsed_comments.append(comment)
                    
                except:
                    continue

            raw.append(raw_comments)
            parsed.append(parsed_comments)
            # preventing 
            time.sleep(0.2)
        
    return raw, parsed

# page names to scrape data from
pages = []

for page in pages:
    print("getting data for {} ...".format(page))
    raw, parsed = getcomments(page)
    print("writing raw data ...")
    with open('{}_raw.json'.format(page), 'w') as outfile:
        json.dump(raw, outfile)

    print("finish writing raw data from {}".format(page))
    print("writing comments ...")
    with open('{}.json'.format(page), 'w') as outfile:
        json.dump(parsed, outfile)
    print("finish writing comments from {}".format(page))





