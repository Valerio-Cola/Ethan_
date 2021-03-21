from bs4 import BeautifulSoup
from urllib.request import urlopen
import pickle
from tweepy import api
from getLink import searcher, truelink
import requests
import tweepy 
import time
import random
import os

time.sleep(1920)

consumer_key = 'jI3PgeF91SzMvWyAijDHB4RlH' 
consumer_secret = 'uHBhZqbrgLEUeQRDNTrnKx48s5sm2dymArsxHnidye28JtgSvf' 
access_token = '1361315303767093248-M4Kk6yzJtlVKiowXhXsZ4sjIgiMEN6' 
access_token_secret = 'eEGVadcC70OyMo7WcwPjJRmCOmddY4VqGq7hyB0WdrEZA' 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


informations = []
id_replace = []
hash_art = ["#artgallery", "#artist", "#artnews", "#artinfo", "#painting", "#paint", "#art", "#drawing", "#colors", "#artwork", "#arte", "#artistic"]

file_name = "Name.pkl"

if os.path.isfile("Name.pkl"):
    
    open_file = open(file_name, "rb")
    id_replace = pickle.load(open_file)  #CARICA
    open_file.close()

else:
    pass

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

        Save_All(id_replace)
        print(informations)
        tweeter()


def tweeter():
    has_name = informations[1].replace(" " ,"")
    has_gen = informations[3][7:].replace(" ","")
    has_gen2 = has_gen[7:].replace("-","")
    has_gen3 = has_gen2[7:].replace(",","")
    last_hash = random.choice(hash_art)
    message = ', '.join(map(str, informations[:2])) + f" {informations[2]} \n\n" + '\n'.join(map(str, informations[3:])) + f"\n\n #{has_name} #{has_gen3} {last_hash}\n" #Source: {truelink[0]}

    media = api.media_upload("sample_image.png")
    api.update_status(status=message, media_ids=[media.media_id])


def Save_All(id_replace):

    open_file = open(file_name, "wb")
    pickle.dump(id_replace, open_file)   #SALVA
    open_file.close()

    open_file = open(file_name, "rb")
    id_replace = pickle.load(open_file)  #CARICA
    open_file.close()

    print(id_replace)


truelink.clear()
informations.clear()
searcher()

print(truelink[0])

url2 = truelink[0]
page2 = urlopen(url2)
html2 = page2.read().decode("utf-8")
soup2 = BeautifulSoup(html2, "html.parser")
    
infogetter()
