from re import A
import requests
from bs4 import BeautifulSoup

# useful links i have been using
# https://realpython.com/beautiful-soup-web-scraper-python/#step-2-scrape-html-content-from-a-page
# https://github.com/psf/requests-html#readme
# https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table

URL = "http://dnd5e.wikidot.com/spells"

page = requests.get(URL)
soup = BeautifulSoup(page.content, "lxml")
results = soup.find(id="page-content")

#Selecting the spell tab (0-9, cantrip-9)
tab1 = soup.find('div', id='wiki-tab-0-0')
data = []
spell_data = []
spell_page_info = []

#should navigate to the link in arg and retrieve the following info as a list:
#Sourcebook
#Components
#Description (with table included) + at higher levels
#Classes that have the spell in their spell list

def spell_page_parser(url):
    spell_page = requests.get(url)
    spell_soup = BeautifulSoup(spell_page.content, 'html.parser')
    spell_soup = spell_soup.find('div', id='page-content')

    rows = spell_soup.find_all('p')


    output = []

    ###Spell source
    spell_source = rows[0]

    output.append(spell_source.text[8:])
    ###Spell source

    ###Spell components 
    components_info = rows[2]
    components_info = components_info.text[components_info.text.find('Components:'):components_info.text.find('Duration:')]

    if '(' in components_info:
        index1 = components_info.find('(') + 1
        index2 = components_info.find(')')
        output.append(components_info[index1:index2])
    else:
        output.append('None')
    ###Spell components 


    ###TODO: Decription parser should be able to handle tables and bullet lists
    ###TODO: orangize each item as an item in a list
    ###NOTE: Tables can also be statblocks http://dnd5e.wikidot.com/spell:summon-celestial
    ### 2nd to last <p> is "At Higher Levels"
    ###NOTE: descriptions may contain 
        # <ul>
        #   <li>
        #   </li>
        # >/ul>
        #for bulleted items
    #EX: http://dnd5e.wikidot.com/spell:greater-restoration
    
    ###TODO: Handle tables in description (probably create a seperate function for this)
    ###Spell descriptions 
    description = rows[3:-1]
    description_text = ""
    for p in description:
        description_text += p.text
        ###TODO: "�" symbol is supposed to be "'"
        description_text = description_text.replace("�", "asfdasdfasdfa")
        output.append(description_text)
    ###Spell descriptions 

    ###Spell Lists 
    spell_lists = rows[-1]
    output.append(spell_lists.text[13:])
    ###Spell Lists 
    
    
    ###I forget wtf this is but its broken (example list formatter probably)
    # for spell in spell_soup:
    #     cols = spell_soup.find_all('p')
    #     cols = [ele.text.strip() for ele in cols]
    #     print(cols)
    ###I forget wtf this is but its broken
    return output


    


###TODO: move the table parser into this function, and try to make it re-usable for all tables
def table_parser(table):
    return 0 #stub


#
table = tab1.find('table', attrs={'class', 'wiki-content-table'})
rows = table.find_all('tr')
# links = table.find_all('a')



###Get info from link in table
# for a in table.find_all('a', href=True):
#     spell_page_info.append(spell_page_parser((URL.replace('/spells', '') + a['href'])))
###Get info from link in table

###ALL SPELLS TABLE PARSE 
for row in rows:
    #get titles and items in table
    cols = row.find_all('th') or row.find_all('td')
    #print(cols)
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])
###ALL SPELLS TABLE PARSE 

#print(spell_page_info)
#spell_page_parser("http://dnd5e.wikidot.com/spell:booming-blade")
# print(len(total_links))
# print(spell_data)
print(data)