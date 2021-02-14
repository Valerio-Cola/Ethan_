from bs4 import BeautifulSoup
from urllib.request import urlopen


truelink = []


def searcher():
    url = "https://www.wikiart.org"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    truelink.append(links[3])
    links.clear()



