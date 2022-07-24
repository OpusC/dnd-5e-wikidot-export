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
spell_data = []
#testing code

#should navigate to the link for each spell and retrieve
#Level, Description + at higher levels
#TODO: Decription parser should be able to handle tables
def get_link_info(url_path):
    #url_path = url_path.replace('/spells', '') #fix url format
    spell_page = requests.get(url_path)
    spell_soup = BeautifulSoup(spell_page.content, 'html.parser')
    spell_soup = spell_soup.find('div', id='page-content')
    for spell in spell_soup:
        cols = spell_soup.find_all('p')
        cols = [ele.text.strip() for ele in cols]
        print(len(cols))
        print(cols)
        break
        ###TODO: orangize each item as an item in a list
        ### First <p> is source (REQUIRED)
        ### Second <p> is school + level (BOTH NOT NEEDED)
        ### Third <p> has casting time, range, components, and duration

        ###NOTE: Components contains duplicate from all spells page of V, S, M, 
        ###BUT also contains gold valued components (Required)

        ### All subsequent <p> is description. There could be several paragraphs, or even tables within this
        ### 2nd to last <p> is "At Higher Levels"
        ### Final <p> is which classes have this spell in the spell list


        ##NOTE: Everything except descrption <p>'s start with <strong>
        #data.append(cols)
        spell_data.append(cols)



#Selecting the spell tab (0-9, cantrip-9)
tab1 = soup.find('div', id='wiki-tab-0-0')
table = tab1.find('table', attrs={'class', 'wiki-content-table'})

rows = table.find_all('tr')
links = table.find_all('a')

total_links = [] ##removable_line

#Get all links in tab
for a in table.find_all('a', href=True):
    temp = a.text.strip()
    total_links.append([temp]) ##testing line
    get_link_info((URL.replace('/spells', '') + a['href']))
    
for row in rows:
    #get titles and items in table
    cols = row.find_all('th') or row.find_all('td')
    #print(cols)
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

# print(len(total_links))
# print(spell_data)
#print(data)