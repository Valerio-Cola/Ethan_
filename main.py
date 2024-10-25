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

# Carica le variabili di ambiente dal file .env in locale se no vengono prese da Heroku
load_dotenv()

# Chiavi e token di accesso a X e Github
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Configura il webdriver di Selenium
def configure_selenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')
    
    # Percorso del ChromeDriver e Google Chrome, i path sono relativi al sistema di Heroku
    chrome_bin = '/app/.chrome-for-testing/chrome-linux64/chrome'  
    chromedriver_path = '/app/.chrome-for-testing/chromedriver-linux64/chromedriver' 
    
    chrome_options.binary_location = chrome_bin
    
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)
    return driver

# Crea un client e un'API per X
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

# Pubblica il post con la relativa immagine 
def tweet(client, api, message, image_path):
    media = api.media_upload(image_path)
    client.create_tweet(text=message, media_ids=[media.media_id])
    print("Tweet inviato: " + message)

# Aggiorna il database su Github, per evitare di pubblicare lo stesso post più volte
# verifica se il titolo e l'autore del quadro sono già presenti nel database, un file .txt
# se non presenti aggiunge il nuovo post al database
def database(titolo, autore):

    g = Github(GITHUB_TOKEN)
    repo = g.get_user().get_repo('EthanStorage')
    
    file = repo.get_contents("db2.txt", ref="main")
    vecchiofile = file.decoded_content.decode()

    new_data = f"{titolo} {autore}"
    
    if new_data not in vecchiofile:
        repo.update_file(file.path, "", f"{vecchiofile}  \n{new_data}", file.sha, branch="main")
        return 0
    else:
        return 1
    

def main():

    # Configura il driver di Selenium
    driver = configure_selenium()

    # Apre il browser e va alla pagina di WikiArt
    driver.get('https://www.wikiart.org/')

    # Trova gli elementi dei link usando XPath
    link = driver.find_elements(By.XPATH, '/html/body/div[2]/div[1]/section/main/div[2]/article/h3/a')


    # estrae il link dell'elemento e cambia pagina
    truelink = link[0].get_attribute('href')
    link[0].click()

    #Le informazioni che voglio estrarre sono contenute in un tag <article>, all'interno di esso ci sono tag <h3> per il titolo,
    #  <h5> per l'autore e <ul> per le varie informazioni, dentro quest'ultimo ci sono tag <li> per ogni informazione
    
    #Il Messaggio viene composto man mano aggiungendo le informazioni estratte, assieme a relative emoji 
    
    # Trova l'elemento <article>
    article = driver.find_element(By.TAG_NAME, 'article')

    # Trova l'elemento <h3> all'interno di <article>
    h3_element = article.find_element(By.TAG_NAME, 'h3')
    print("H3 Element: ", h3_element.text)
    msg = f"\U0001f5bc {h3_element.text}"

    # Trova l'elemento <h5> all'interno di <article>
    h5_element = article.find_element(By.TAG_NAME, 'h5')
    print("H5 Element: ", h5_element.text)
    msg += f",{h5_element.text}"

    msg += "\n\n"

    # Trova l'elemento <li> all'interno di <ul> all'interno di <article> relativo al luogo in cui si trova l'opera
    # Spesso non è presente quindi è necessario gestire l'eccezione
    try:
        ul_element = article.find_element(By.TAG_NAME, 'ul')
        li_elements = ul_element.find_element(By.CLASS_NAME, 'dictionary-values-gallery')

        # Estrae il contenuto dei tag <s> e <span>
        s_element = li_elements.find_element(By.TAG_NAME, 's').text
        span_element = li_elements.find_element(By.TAG_NAME, 'span').text
        print(s_element+ " " + span_element)

        msg += f"\U0001F3DB {s_element} {span_element}\n"

    except:
        print('NO LUOGO')
    
    # Trova i restanti elementi <li>  
    li_elements = ul_element.find_elements(By.CLASS_NAME, 'dictionary-values')

    # Itera su ognuno di essi e estrae il contenuto dei tag <s> e <span>
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

    # Trova l'elemento immagine con itemprop="image"
    image_element = driver.find_element(By.XPATH, '//img[@itemprop="image"]')
    image_url = image_element.get_attribute('src')

    # Scarica l'immagine
    image_data = requests.get(image_url).content
    with open('quadro.jpg', 'wb') as file:
        file.write(image_data)
    file.close()
    
    # Hashtag per il post
    hash_art = ["#artist", "#artnews", "#artinfo", "#painting", "#paint", "#art", "#drawing", "#colors", "#artwork", "#arte", "#artistic"]
    
    msg += f"\n#{h5_element.text.replace(' ', '')} #art #artgallery {random.choice(hash_art)}\n\U0001F517 {truelink}"

    # Verifica se il post è già presente nel database
    if database(h3_element.text, h5_element.text) == 1:
        return
    else:
        # Crea il client e l'API per X e pubblica il post
        print(msg)
        client, api = create_client()
        tweet(client, api, msg, 'quadro.jpg')

    # Chiudi il driver
    driver.quit()
    



    
if __name__ == "__main__":
    main()
