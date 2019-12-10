import requests
import re
from bs4 import BeautifulSoup


class Article():
    '''Model of an online article for quotation and citation'''

    def __init__(self, title, content, pub_date, access_date, url, ref_citation, parenthetical, author="National Instititute of Mental Health"):
        self.title = title
        self.content = content
        self.pub_date = pub_date
        self.access_date = access_date
        self.url = url
        self.ref_citation = ref_citation
        self.parenthetical = parenthetical
        self.author = author


def clean_string(string):
    new_string = re.findall(r'(?<=>).*(?=<)', str(string))[0]
    return new_string


def find_content(content_data):
    '''
    Go through HTML from BeautifulSoup to get_text() from all <p> and <li> tags
    li_dict should be able to show me which <li> tags correspond to what previous sentence
    This way I can display any lists as entire pieces of data, not as single lines of info
    However all <li> tags are also in content list
    
    '''
    content = []
    li_dict = {}
    for i in range(0, len(content_data)):
        not_done_yet = True
        for val_list in li_dict.values():
            if content_data[i] in val_list:
                not_done_yet = False
        if not_done_yet:
            try:
                content_data[i].get_text()
                content_data[i - 1]
            except Error:
                continue
            else:
                piece = content_data[i].get_text()
                if '<li' in str(piece):
                    list_items = []
                    li_dict[content_data[i - 1]] = list_items
                    for datum in content_data[i:]:
                        if '<li' in datum:
                            list_items.append(datum)
                        else:
                            break
                    if li_dict:
                        content.append(li_dict)
                else:
                    if piece and len(str(piece)) > 20:
                        content.append(piece)
        else:
            continue

    return content


def scrape_nimh_page(href):

    #get specific page to be scraped
    url = ('https://www.nimh.nih.gov' + href)
    try:
        page = requests.get(url)
    except Error:
        return print('REQUEST FAILED AT:' + url)

    soup = BeautifulSoup(page.text, 'html.parser')

    #locate main content via id
    article = soup.find('article', id="main_content_inner")

    #screen out newlines
    data_list = [x for x in article if str(
        type(x)) == "<class 'bs4.element.Tag'>"]

    #locate title of the page
    title_data = soup.find('h1', id="title")

    #Remove parts of string left over from HTML tags
    article_title = clean_string(title_data)

    #Define article_content
    content_data = soup.main.find_all(['p', 'li'])
    article_content = find_content(content_data)

    #Define other article variables
    article_url = url

    return print(article_title + ' first data piece: ' + article_content[0][:40] + '...')


#def __init__(self, title DONE, author DONE, content DONE, pub_date, access_date, url DONE, ref_citation, parenthetical):

#'/health/topics/index.shtml'

def define_nimh_href_list(directory):
    page_02 = requests.get('https://www.nimh.nih.gov' + directory)
    soup_02 = BeautifulSoup(page_02.text, 'html.parser')
    link_data = [x for x in soup_02.main.find_all('li')]
    href_list = []
    for i in range(0, len(link_data)):
        href = re.findall(r'(?<=href=")[^\s].*[^\s](?="\s)', str(link_data[i]))
        href_list.append(href[0])

    return href_list


def scrape_nimh_pages(directory):

    href_list = define_nimh_href_list(directory)

    for href in href_list:
        scrape_nimh_page(href)


site = '/health/topics/index.shtml'
scrape_nimh_pages(site)
