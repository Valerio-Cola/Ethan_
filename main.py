from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

from getLink import searcher, truelink
import time
import random

##cFpHd05WaGhoNW1lYlMyU3U4RVQ6MTpjaQ zSB8jgFacOxeNzp1hFJARRwDFC2UyGSDRjVuKroWZfMKrxKJmk 
###---Login into TwitterAPI---###
from tweepy import api
import tweepy 

consumer_key = 'QpZSniG92kP23NFvtMdlkn0s8' 
consumer_secret = 'nOljbT3D4WiG0cbZhsXKxMo4wXkXyt5PmcwB4kK07dNC9WQ9TJ' 
access_token = '1595096122472763400-9tJnGFPeqyNMlXvlqiP2ogRq7iiFYk' 
access_token_secret = 'dm00LwgKOK4zBu8HpqzbiLGiXn1PIBFknOcurEharU2Xz' 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)




###---Get Informations about the link---###

informations = []

def infogetter():

    # Get title
    titles = soup2.find("h1") 
    informations.append("\U0001f5bc\uFE0F" + titles.text)
    
    # Get author
    author = soup2.find("h2")   
    informations.append(author.text)
    
    # Get image
    img = soup2.find(itemprop= "image") 
    image1 = img.get("src")
    response = requests.get(image1)
    file = open("sample_image.png", "wb")
    file.write(response.content)
    file.close()
    
    # Get date
    for z in soup2.find_all("span", attrs={"itemprop":"dateCreated"}): 
        z1 = z.get_text()
        informations.append(z1)
    
    # Get generic informations
    for x in soup2.find_all("li", attrs={"class":"dictionary-values"}): 
        x1 = x.text
        x2 = x1.replace("\n", "")
        x3 = x2[:6]
        informations.append(x3 + " " + x2[6:])

    # Get gallery location
    for y in soup2.find_all("li", attrs={"class":"dictionary-values-gallery"}): 
        y1 = y.get_text()
        y2 = y1.replace("\n", "")
        y3 = y2.replace("Location:" , "")
        informations.append("\U0001f4cd Location: " + y3)

    print(informations)
    duplicate_finder(titles, author)



###---Search if the same tweet already exist---###

def duplicate_finder(titles, author):

    duplicated = titles.text + ", " + author.text
        
    lista_query = []
    tweets = api.user_timeline(screen_name = "Ethan Algorithm", count = 50, include_rts = False, tweet_mode = 'extended')

    for info in tweets:
         appended = info.full_text
         appended1 = appended.replace("\n","")
         index = appended1.find("Style")
         lista_query.append(appended1[:int(index)])

    if duplicated in lista_query:
        return
    else:
        tweeter()


###---Publish the tweet---###

hash_art = ["#artist", "#artnews", "#artinfo", "#painting", "#paint", "#art", "#drawing", "#colors", "#artwork", "#arte", "#artistic"]

def tweeter():
    has_name = informations[1].replace(" " ,"")
    last_hash = random.choice(hash_art)
    last_hash2 = random.choice(hash_art)
    

    message = ', '.join(map(str, informations[:2])) + f" {informations[2]}\n\n" + "\U0001f3a8" + '\n'.join(map(str, informations[3:])) + f"\n\n #{has_name} #art #artgallery {last_hash} {last_hash2}\n Source: {truelink[0]}"
    
    media = api.media_upload("sample_image.png")
    api.update_status(status=message, media_ids=[media.media_id])


###---Call the function of getLink.py---###

searcher()



###---Enter into the link with bs4 obtained with getLink.py---###

url2 = truelink[0]
page2 = urlopen(url2)
html2 = page2.read().decode("utf-8")
soup2 = BeautifulSoup(html2, "html.parser")



###---Get Informations about the link---###

infogetter()



time.sleep(1800) # 30 min

