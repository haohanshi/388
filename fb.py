import requests
import json

access_token = "1697206690593876|fcac71a66e40681733a5908f2fd0f75b"
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
            
msg, id = getpost("barackobama")


def getcomments(pagename):
    idlist = getpost(pagename)[1]
    comment = []
    for id in idlist:
        url = "https://graph.facebook.com/v2.8/" + id + "/comments?access_token=" + access_token
        comment.append(requests.get(url).text)
    return comment
print getcomments("barackobama")
