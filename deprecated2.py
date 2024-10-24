###---Get link for the artwork with selenium, using bs4 it doesn't work because the link is incorporated into a ViewModel---###
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
truelink = []
links = []



def searcher():
    driver = webdriver.ChromeOptions()
    driver.add_argument("disable-dev-shm-usage")
    gdriver = webdriver.Chrome(
    chrome_options=driver, executable_path=ChromeDriverManager().install())
    gdriver.get('https://www.wikiart.org/')
    b = gdriver.find_elements(By.XPATH, "/html/body/div[2]/div[1]/section/main/div[2]/article/ul/li[2]/a")
    for a in b:
        links.append(a.get_attribute('href'))
    truelink.append(links[0])
    links.clear()

