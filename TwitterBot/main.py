from bs4 import BeautifulSoup
from urllib.request import urlopen
from getLink import searcher, truelink
import requests
import tweepy 
import time

consumer_key = 'cJGILwxzmlcr59Jbkwta9O0nM' 
consumer_secret = 'FYplFtMriP5rxOySgnBMfM4rAlzlST9v19fGzVF3RoeGULgGSe' 
access_token = '1356642176021708802-6m6Y1W4SE4tTv8K4i0pS8vYILCXNYH' 
access_token_secret = 'VSloJBx85qUKBTuBAPhaKnB0VMouQEpZhz2GBBnrzsOCr' 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

informations = []
id_replace =[]

def infogetter():

    titles = soup2.find("h1")
    
    if titles.text in id_replace:
        return
    else:
        id_replace.append(titles.text)
        informations.append(titles.text)

        author = soup2.find("h2")
        informations.append(author.text)

        img = soup2.find("img")
        image1 = img.get("src")
        response = requests.get(image1)
        file = open("sample_image.png", "wb")
        file.write(response.content)
        file.close()

        for z in soup2.find_all("span", attrs={"itemprop":"dateCreated"}):
            z1 = z.get_text()
            informations.append(z1)

        for x in soup2.find_all("li", attrs={"class":"dictionary-values"}):
            x1 = x.text
            x2 = x1.replace("\n", "")
            x3 = x2[:6]
            informations.append(x3 + " " + x2[6:])

        for y in soup2.find_all("li", attrs={"class":"dictionary-values-gallery"}):
            y1 = y.get_text()
            y2 = y1.replace("\n", "")
            y3 = y2.replace("Location:" , "")
            informations.append("Location: " + y3)

        print(informations)
        tweeter()


def tweeter():
    has_name = informations[1].replace(" " , "")
    has_gen = informations[3][7:]
    message = ', '.join(map(str, informations[:2])) + f" {informations[2]} \n\n" + '\n'.join(map(str, informations[3:])) + f"\n\n #{has_name} #{has_gen} #art #arte "
    
    media = api.media_upload("sample_image.png")
    api.update_status(status=message, media_ids=[media.media_id])
 

while True:
    truelink.clear()
    informations.clear()

    searcher()

    print(truelink[0])
    url2 = truelink[0]
    page2 = urlopen(url2)
    html2 = page2.read().decode("utf-8")
    soup2 = BeautifulSoup(html2, "html.parser")
 
    infogetter()
    time.sleep(2100)
    
    
