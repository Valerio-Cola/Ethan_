###---Get link for the artwork with selenium, using bs4 it doesn't work because the link is incorporated into a ViewModel---###

from selenium import webdriver

truelink = []
links = []

def searcher():
    driver = webdriver.Chrome()
    driver.get('https://www.wikiart.org/')
    for a in driver.find_elements_by_tag_name('a'):
        links.append(a.get_attribute('href'))
    truelink.append(links[65])
    links.clear()

