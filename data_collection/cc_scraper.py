from bs4 import BeautifulSoup
import requests
import string
import json

# this file scrapes comments from college confidential website, and the
# collected data will belong to the high school category 

def getcomment(turl, index):
    comment = []
    for i in range(1, index + 1):
        if i == 1:
            url = turl + ".html"
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            set = soup.findAll("div", class_="Message")
            for element in set:
                comment.append(element.contents[0].strip())
        else:
            p = "-p" + str(i)
            url = turl + p + ".html"
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            set = soup.findAll("div", class_="Message")
            for element in set:
                comment.append(element.contents[0].strip())
    return comment

# pages selected to collect from college confidential
turl1 = "https://talk.collegeconfidential.com/sat-preparation/1788088-october-2015-sat-us-only-thread"
index1 = 206
turl2 = "https://talk.collegeconfidential.com/sat-preparation/1826999-march-2016-sat-us-only-thread-new-redesigned-sat-discussion-thread"
index2 = 59
turl3 = "https://talk.collegeconfidential.com/sat-preparation/1800000-january-2016-sat-us-only-thread"
index3 = 75
turl4 = "https://talk.collegeconfidential.com/sat-preparation/1854691-february-2016-sat-makeup-thread"
index4 = 94


total = []

with open('college_confidential.json', 'w') as outfile:
    print ("getting 1st page...")
    comment1 = getcomment(turl1, index1)
    print ("getting 2nd page...")
    comment2 = getcomment(turl2, index2)
    print ("getting 3rd page...")
    comment3 = getcomment(turl3, index3)
    print ("getting 4th page...")
    comment4 = getcomment(turl4, index4)      
    total = comment1 + comment2 + comment3 + comment4
    print ("dumping data...")
    json.dump(total, outfile)



