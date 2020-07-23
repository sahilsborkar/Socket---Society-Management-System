from bs4 import BeautifulSoup
import time
import requests
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
import json

import pprint

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://manchesterstudentsunion.com/groups/")
time.sleep(1)

while True:
#for i in range (0,3):
    try:
        loadMoreButton = driver.find_element_by_xpath("//a[@class='uc-load-more-groups']")
        time.sleep(1)
        loadMoreButton.click()
        time.sleep(2)
    except Exception as e:
        print(e)
        break

page = driver.page_source
soup = BeautifulSoup(page, "lxml")
results = soup.find(id='right-content')
tags = results.select("a.group-box[href]")
json_list = []

base_link = "https://manchesterstudentsunion.com"
tag_list = []
for t in tags:
    tag_list.append(t['href'])

desc_elem = []

for t in tag_list:
    print(t)
    dictionary = {}
    real_link = base_link + t
    URL = real_link
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='uc-groups-details-page')
    if results is None:
        pass
    else:
        name_elem = results.h1
        dictionary["name"] = name_elem.get_text()
        desc_group = results.find_all("p")
        if len(desc_group) != 0:
            #if '\n' in desc_group[0] or '\r' in desc_group[0] or '\u00a0' in desc_group[0] or '\u2019' in desc_group[0]:
                #desc_elem = desc_group[0].replace(['\n', '\r', '\u00a0', '\u2019'], ' ')
            #else:
            desc_elem = desc_group[0]
            if '\n' in desc_elem.get_text() or '\r' in desc_elem.get_text() or '\t' in desc_elem.get_text():
                dictionary["description"] = desc_elem.get_text().replace('\n', ' ').replace('\r', ' ').replace('\t', '')
            else:
                dictionary["description"] = desc_elem.get_text()
        else:
            desc_elem = "No description"
            dictionary["description"] = desc_elem
        json_list.append(dictionary)

json_obj = json.dumps(json_list)

with open('/home/sahil/Desktop/ProgrammingProjects/project_socket/societies.json', 'w+') as fout:
    json.dump(json_list , fout,indent=4)