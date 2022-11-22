###---Get link for the artwork with selenium, using bs4 it doesn't work because the link is incorporated into a ViewModel---###
from selenium.webdriver.common.by import By
from selenium import webdriver

truelink = []
links = []



def searcher():
    driver = webdriver.Chrome()
    driver.get('https://www.wikiart.org/')
    b = driver.find_elements(By.XPATH, "/html/body/div[2]/div[1]/section/main/div[2]/article/ul/li[2]/a")
    for a in b:
        links.append(a.get_attribute('href'))
    truelink.append(links[0])
    links.clear()
