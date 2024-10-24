import random
import tweepy
from tweepy import api

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests

from github import Github

import os
from dotenv import load_dotenv

# Carica le variabili di ambiente dal file .env se esiste
load_dotenv()


# Le chiavi e i token di accesso di Twitter
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


def configure_selenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')
    
    # Percorso del ChromeDriver installato dal buildpack
    chrome_bin = os.getenv('GOOGLE_CHROME_BIN', '/app/.apt/usr/bin/google-chrome')
    chromedriver_path = os.getenv('CHROMEDRIVER_PATH', '/app/.chromedriver/bin/chromedriver')
    
    chrome_options.binary_location = chrome_bin
    
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)
    return driver

def create_client():
    
    auth = tweepy.OAuth1UserHandler(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )

    api = tweepy.API(auth)
    
    try:
        api.verify_credentials()
        print("Autenticazione avvenuta con successo")
    except tweepy.TweepyException as e:
        print("Errore durante l'autenticazione", e)
    
    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    
    return client, api

def tweet(client, api, message, image_path):
    media = api.media_upload(image_path)
    client.create_tweet(text=message, media_ids=[media.media_id])
    print("Tweet inviato: " + message)

def database(titolo, autore):

    g = Github(GITHUB_TOKEN)
    repo = g.get_user().get_repo('EthanStorage')
    
    # update
    file = repo.get_contents("db2.txt", ref="main")
    vecchiofile = file.decoded_content.decode()

    new_data = f"{titolo} {autore}"
    
    if new_data not in vecchiofile:
        repo.update_file(file.path, "", f"{vecchiofile}  \n{new_data}", file.sha, branch="main")
        return 0
    else:
        return 1
    

def main():

    driver = configure_selenium()
    driver.get('https://www.wikiart.org/')

    # Trova gli elementi dei link usando XPath
    link = driver.find_elements(By.XPATH, '/html/body/div[2]/div[1]/section/main/div[2]/article/h3/a')


    truelink = link[0].get_attribute('href')

    # Clicca sul link
    link[0].click()

    # Trova l'elemento <article>
    article = driver.find_element(By.TAG_NAME, 'article')

    h3_element = article.find_element(By.TAG_NAME, 'h3')
    print("H3 Element: ", h3_element.text)
    msg = f"\U0001f5bc {h3_element.text}"

    # Trova l'elemento <h5> all'interno di <article>
    h5_element = article.find_element(By.TAG_NAME, 'h5')
    print("H5 Element: ", h5_element.text)
    msg += f",{h5_element.text}"

    msg += "\n\n"
    try:
        ul_element = article.find_element(By.TAG_NAME, 'ul')
        li_elements = ul_element.find_element(By.CLASS_NAME, 'dictionary-values-gallery')

        s_element = li_elements.find_element(By.TAG_NAME, 's').text
        span_element = li_elements.find_element(By.TAG_NAME, 'span').text
        print(s_element+ " " + span_element)
        print()
        msg += f"\U0001F3DB {s_element} {span_element}\n"

    except:
        print('NO LUOGO')
    

    li_elements = ul_element.find_elements(By.CLASS_NAME, 'dictionary-values')

    # Itera sugli elementi <li> e stampa il contenuto dei tag <s> e <span>
    for li in li_elements:
        s_element = li.find_element(By.TAG_NAME, 's').text
        span_element = li.find_element(By.TAG_NAME, 'span').text
        print(s_element)
        print(span_element)
        if s_element == "Style:":
            msg += "\U0001f3a8"
        elif s_element == "Media:":
            msg += "\U0001F58C"

        msg += f"{s_element} {span_element}\n"

    # Trova l'elemento dell'immagine con itemprop="image"
    image_element = driver.find_element(By.XPATH, '//img[@itemprop="image"]')
    image_url = image_element.get_attribute('src')

    # Scarica l'immagine
    image_data = requests.get(image_url).content
    with open('quadro.jpg', 'wb') as file:
        file.write(image_data)
    file.close()
    
    hash_art = ["#artist", "#artnews", "#artinfo", "#painting", "#paint", "#art", "#drawing", "#colors", "#artwork", "#arte", "#artistic"]
    
    
    msg += f"\n#{h5_element.text.replace(' ', '')} #art #artgallery {random.choice(hash_art)}\n\U0001F517 {truelink}"

    if database(h3_element.text, h5_element.text) == 1:
        return
    else:
        print(msg)
        client, api = create_client()
        tweet(client, api, msg, 'quadro.jpg')

    # Chiudi il driver
    driver.quit()




    
if __name__ == "__main__":
    main()
