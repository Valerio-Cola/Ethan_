from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

from getLink import searcher, truelink
import time
import random



###---Login into TwitterAPI---###
from tweepy import api
import tweepy 

consumer_key = 'CG6xRJT6tyzmtU02VFKBsJ7vb' 
consumer_secret = 'grValF0HVRr2edhKzqM72xe2ytXrVu5wj4PbhSwYTV0j1fjYVK' 
access_token = '1432301626757353472-A74aSFk5cn0RPNfIZJF4AxqLDOd4s5' 
access_token_secret = 'p0KqKbSnFMv2gnffKjr9Ilt7hZwhP5EXbWFfgmVeICjmU' 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)



###---Get Informations about the link---###

informations = []

def infogetter():

    # Get title
    titles = soup2.find("h1") 
    informations.append(titles.text)
    
    # Get author
    author = soup2.find("h2")   
    informations.append(author.text)
    
    # Get image
    img = soup2.find("img") 
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
        informations.append("Location: " + y3)

    print(informations)
    duplicate_finder(titles, author)



###---Search if the same tweet already exist---###

def duplicate_finder(titles, author):

    duplicated = titles.text + ", " + author.text
        
    lista_query = []
    tweets = api.user_timeline(screen_name = "EthanAlgo", count = 50, include_rts = False, tweet_mode = 'extended')

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

    message = ', '.join(map(str, informations[:2])) + f" {informations[2]}\n\n" + '\n'.join(map(str, informations[3:])) + f"\n\n #{has_name} #art #artgallery {last_hash}\n Source: {truelink[0]}"

    media = api.media_upload("sample_image.png")
    api.update_status(status=message, media_ids=[media.media_id])



###---Call the function of getLink.py---###

searcher()



###---Enter into the link with bs4 obtained with getLink.py---###

print(truelink[0])
url2 = truelink[0]
page2 = urlopen(url2)
html2 = page2.read().decode("utf-8")
soup2 = BeautifulSoup(html2, "html.parser")



###---Get Informations about the link---###

infogetter()




###---Wait to avoid that twitterAPI session is too long open---###  

time.sleep(3600) # 1 hour
