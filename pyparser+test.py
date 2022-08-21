
import requests

from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry



requests.adapters.DEFAULT_RETRIES = 20
session = requests.Session()
retry = Retry(connect = 3, backoff_factor=2)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# useful links i have been using
# https://realpython.com/beautiful-soup-web-scraper-python/#step-2-scrape-html-content-from-a-page
# https://github.com/psf/requests-html#readme
# https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table

###TODO: put table_getter function in , then begin the yaml file export

URL = "http://dnd5e.wikidot.com/spells"

##gets all the tabs with spell tables from cantrip to lvl 9
def get_all_tabs():
    page = session.get(URL, verify=False)
    soup = BeautifulSoup(page.content, 'lxml')
    soup = soup.find('div', id='page-content')
    tabs = soup.find("div", {"class": "yui-content"}).findChildren(recursive=False)
    return tabs

def spell_page_parse(url):
    page = session.get(url, verify=False)
    soup = BeautifulSoup(page.content, 'lxml').find('div', id='page-content')
    page.close()
    components = get_spell_components(soup.find_all('p')[2])
    bullets = ['Bullets']
    table = ['Table']

    if soup.find_all('ul') != []:
        bullets = get_bullet_points(soup.find_all('ul'))
    if soup.find('table') != None:
        table = check_and_get_table(soup.find('table')) #this one if for the clicked link
    spell_lists = [x.strip() for x in soup.find_all('p')[-1].text[13:].split(',')] #http://dnd5e.wikidot.com/spell:control-flames i think bullet points are fuckking up

    output = [components, bullets, table, spell_lists]
    
    return output


# def get_spell_tab_info(table):
#     rows = table.find_all('tr')
#     output = []
#     output.append(rows[0].find_all('th').text)
#     for row in rows[1:]:
#         cols = row.find_all('td')
#         cols = [ele.text.strip() for ele in cols]
#         link = row.find('a', href=True)
#         cols.append(spell_page_parse(link))
#         output.append(cols)
#     return output

#format statblock like https://github.com/valentine195/obsidian-5e-statblocks
def get_statblock(table):
    return ('Statblock found')

#input is a table
#get all columns and rows

def get_table(table):
    output = []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('th') or row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        spell_page_info = []
        if row.find('a') != None:
            url = row.find('a', href=True)['href'].replace('http://dnd5e.wikidot.com', '')
            spell_page_info = spell_page_parse(URL[0:-7] + url)
            #spell_page_parse(URL[0:-7] + url['href'])            
        output.append([ele for ele in cols if ele] + spell_page_info)
    return output


def spell_tab_parse(tab):
    output = []
    table = tab.find('table')
    output.append(get_table(table))

    return output

#change to recieve all <ul> and not url

def get_bullet_points(bullets): #idk this is broken or something
    bullet_text = []
    for bullet in bullets:
        #TODO: get title of some bullet points ex http://dnd5e.wikidot.com/spell:true-polymorph  , some '\n' shenanigans
        bullet = bullet.find('li')
        bullet_text.append(unicode_fixer(bullet.text))
    return bullet_text

#fix random ass unicode fuckery
def unicode_fixer(text):
    return ((str(text.encode('utf-8', 'ignore'))).replace("\\xe2\\x80\\x83", "").replace("\\xe2\\x80\\x94", "").replace('\\xe2\\x80\\x99', "'")
    .replace('\\xe2\\x80\\x94', ' ').replace('\\u2212', '-').replace('\\xe2\\x80\\x93', '-').replace('\\xe2\\x80\\x93\\xc2\\xa0', '-')[2:-1])

#should navigate to the link in arg and retrieve the following info as a list: 
#Sourcebook, Components, Description (with tables + bullets + at higher levels, Classes)
def all_spells_parser():
    #Selecting all spell tabs (0-9, cantrip-9)
    tabs = get_all_tabs()
    output = []

    for tab in tabs:
        output.append(spell_tab_parse(tab))

    return output

##takes in the <p> with casting time, range, components, duration
#output 
def get_spell_components(components_info):
    components_info = components_info.text[components_info.text.find('Components:'):components_info.text.find('Duration:')]

    if '(' in components_info:
        index1 = components_info.find('(') + 1
        index2 = components_info.find(')')
        components =  components_info[index1:index2]
        components = unicode_fixer(components)

        ##TODO: http://dnd5e.wikidot.com/spell:healing-elixir-ua UA ONES HAVE EDITOR NOTES THAT FUCK SHIT UP

    else:
        components = 'None'
    
    return components

#TODO:change this to take in a table and not a url, then move into spell_page_parser function
def check_and_get_table(table):
    headers_num = len(table.find_all('th'))
    if (headers_num == 8 or 9):
        return (get_statblock(table))
    else:
        return (get_table(table))

###LINK FROM TABLE GETTER

###Get info from link in table
# for a in table.find_all('a', href=True):
#     spell_page_info.append(spell_page_parser((URL.replace('/spells', '') + a['href'])))
###Get info from link in table

###ALL SPELLS TABLE PARSE 
# for row in rows:
#     #get titles and items in table
#     cols = row.find_all('th') or row.find_all('td')

#     cols = [ele.text.strip() for ele in cols]
#     data.append([ele for ele in cols if ele])
###ALL SPELLS TABLE PARSE

###merges each element 2 2d lists
#ex a = [[1, 2, 3],[4, 5, 6]]
# b = [[7,8,9],[4,5,5]]
# output = [[1,2,3,7,8,9], [4,5,6,4,5,5]]
def combine_lists(list1, list2):
    output = []
    for ele1, ele2 in zip(list1, list2):
        output.append(ele1 + ele2)
    
    return output


############ Test prints lol ############


# all_spell_info = combine_lists(data[1:], spell_page_info)
# print(all_spell_info)
###comine lists

#print(spell_page_info[0])

# print(len(spell_page_info))
# print(len(data))
#print(all_spells_parser())
print(all_spells_parser())
# print(len(total_links))
# print(spell_data)
#print(len(data[1:]))

# table_test1_url = "http://dnd5e.wikidot.com/spell:summon-celestial"
# table_test2_url = "http://dnd5e.wikidot.com/spell:teleport"
# table_test1 = requests.get(table_test1_url)
# table_test2 = requests.get(table_test2_url)
# table_test1 = BeautifulSoup(table_test1.content, 'lxml')
# table_test2 = BeautifulSoup(table_test2.content, 'lxml')
# table_test1 = table_test1.find('table')
# table_test2 = table_test2.find('table')




