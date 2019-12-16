import requests
import re
from requests.exceptions import Timeout


def get_url():
    def get_request():
        print('Enter search query:')
        request = str(input())

        return request

    def key_controls(message):
        key = 0

        while key != 1 and key != 2:
            print(message)
            try:
                key = int(input())
                if key == 3: exit()
            except ValueError:
                print('ValueError')
            except KeyboardInterrupt:
                print('KeyboardInterrupt, for exit press 3')

        if key == 1: return True
        else: return False

    def choose_site():
        message = 'Press 1 for search in google.com or 2 for search in ya.ru. 3 for exit'
        choosen_site = key_controls(message)

        if choosen_site:
            site = 'https://www.google.com/search?q='
        else:
            site = 'https://yandex.ru/search/?text='

        return site

    def recursive_search():
        message = 'Press 1 if you need recursive search or 2 if not. 3 for exit'
        recursive = key_controls(message)

        return recursive

    request = get_request()
    site = choose_site()
    recursive = recursive_search()
    url = site + request

    return url, recursive


def get_links(url, recursive):
    dirty_links = []
    links = []

    try:
        page = requests.get(url, timeout=5).text
    except requests.exceptions.ConnectionError:
        print('ConnectionError')
        return links
    except Timeout:
        print('Timeout')
        return links

    dirty_links = page.split('href="')

    for dirty_link in dirty_links:
        dirty_link = re.sub(r'^.*http', 'http' , dirty_link)
        if re.match(r'(http|https)://', dirty_link) is not None:
            links.append(re.sub(r'[\s\"<>\]].*', '', dirty_link))

    if not recursive:
        return links
    else:
        child_links = []
        for link in links:
            for child in get_links(link, False):
                child_links.append(child)

        return links + child_links


def print_recieved_links(links, recursive):
    def get_number_of_links(links):
        number_of_links = len(links) 
        input_number_of_links = 0

        print(f'Found {len(links)} links. Enter numbers of links to display:')
        while input_number_of_links == 0:
            try: 
                input_number_of_links = int(input())
                if number_of_links < input_number_of_links:
                    input_number_of_links = 0
                    print(f'Entered number more then {number_of_links}, try again:')
            except ValueError:
                print('Need number')
    
        return input_number_of_links

    input_number_of_links = get_number_of_links(links)

    for i,link in enumerate(links):
        if i < input_number_of_links:
            print(i+1,'-',link)


