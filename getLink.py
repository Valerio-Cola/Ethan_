from selenium import webdriver
driver = webdriver.Chrome()

truelink = []
links = []


def searcher():
    driver.get('https://www.wikiart.org/')
    for a in driver.find_elements_by_tag_name('a'):
        links.append(a.get_attribute('href'))
    truelink.append(links[65])
    links.clear()

searcher()