from bs4 import BeautifulSoup
import requests
import string
def getcomment(turl, index):
    comment = []
    for i in range(1, index + 1):
        print i
        if i == 1:
            url = turl + ".html"
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            set = soup.findAll("div", class_="Message")
            for element in set:
                comment.append(string.strip(element.contents[0]))
        else:
            p = "-p" + str(i)
            url = turl + p + ".html"
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            set = soup.findAll("div", class_="Message")
            for element in set:
                comment.append(string.strip(element.contents[0]))
    return comment
turl1 = "https://talk.collegeconfidential.com/sat-preparation/1788088-october-2015-sat-us-only-thread"
index1 = 206
turl2 = "https://talk.collegeconfidential.com/sat-preparation/1826999-march-2016-sat-us-only-thread-new-redesigned-sat-discussion-thread"
index2 = 59
turl3 = "https://talk.collegeconfidential.com/sat-preparation/1800000-january-2016-sat-us-only-thread"
index3 = 75
turl4 = "https://talk.collegeconfidential.com/sat-preparation/1854691-february-2016-sat-makeup-thread"
index4 = 94
comment1 = getcomment(turl1, index1)
comment2 = getcomment(turl2, index2)
comment3 = getcomment(turl3, index3)
comment4 = getcomment(turl4, index4)      
total = comment1 + comment2 + comment3 + comment4

    

