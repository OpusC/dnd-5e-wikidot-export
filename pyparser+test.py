import requests
from bs4 import BeautifulSoup

# useful links i have been using
# https://realpython.com/beautiful-soup-web-scraper-python/#step-2-scrape-html-content-from-a-page
# https://github.com/psf/requests-html#readme
# https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table

URL = "http://dnd5e.wikidot.com/spells"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="page-content")

data = []
#testing code

#Selecting the spell tab (0-9, cantrip-9)
tab1 = soup.find('div', id='wiki-tab-0-0')
table = tab1.find('table', attrs={'class', 'wiki-content-table'})

rows = table.find_all('tr')
links = table.find_all('a')

#Get all links in tab
for a in table.find_all('a', href=True):
    print ("URL=", a['href'])


for row in rows:
    #get titles and items in table
    ###TODO: getting more info from clicking link
    #links = row.find_all('a')
    

    cols = row.find_all('th') or row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])



#print(data)


#should navigate to the link for each spell and retrieve
#Level, Description + at higher levels
#Decription parser should be able to handle tables
def get_link_info():
    return #stub