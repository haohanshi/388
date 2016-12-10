import requests
import json
import pandas
import time

app_id = "1786012341650556"
app_secret = "deaada8ad48ddb190897068758c4d0ae"
access_token = app_id + "|" + app_secret


def getid(pagename):
    url = "https://graph.facebook.com/" + pagename + "?access_token=" + access_token
    text = str(requests.get(url).text)
    index = text.find('id":"')
    return text[index+5:-2]

def getpost(pagename):
    msg = []
    idl = []
    id = getid(pagename)
    url = "https://graph.facebook.com/v2.8/" + id + "/posts/?fields=message&limit=100&access_token=" + access_token
    text = requests.get(url).text
    data = json.loads(text, strict=False)
    for set in data["data"]:
        if "message" in set:
            msg.append(set["message"])
        if "id" in set:
            idl.append(set["id"])
    return msg, idl
            
#messages, ids = getpost("nytimes")
#
#for msg in messages:
#    try:
#        print (msg)
#    except:
#        pass
    

def getcomments(pagename):
    idlist = getpost(pagename)[1]
    parsed = []
    raw = []

    num_comments = 0
    while num_comments < 2000:
        for id in idlist:
            url = "https://graph.facebook.com/v2.8/" + id + "/comments?access_token=" + access_token
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
                    
                    if (len(comment.split(" ")) > 5):
                        num_comments += 1
                        parsed_comments.append(comment)
                except:
                    continue

            raw.append(raw_comments)
            parsed.append(parsed_comments)
            time.sleep(0.2)
        
    return raw, parsed

#nytimes_comment = getcomments("nytimes")
#print (nytimes_comment)
#newyorkers_comment = getcomments("newyorker")


pages = [
'nytimes',
'newyorker',
'TheEconomist',
'justin.bieber.film',
'TwilightMovie',
'minecraft',
'clubpenguin'
]

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



