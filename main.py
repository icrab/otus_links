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
            except ValueError:
                print('ValueError')
            except KeyboardInterrupt:
                print('KeyboardInterrupt, for exit press 3')

            if key == 3:
                exit()

        return key

    def choose_site():
        message = 'Press 1 for search in google.com or 2 for search in ya.ru. 3 for exit'
        choosen_site = key_controls(message)

        if choosen_site == 1:
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


def get_links(url):
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
            links.append(re.sub(r'[\s\"<>].*', '', dirty_link))

    return links


def print_get_links(links, recursive):
    for link in links:
        print('From main page:\n', link)
        if recursive == 1:
            child_links = get_links(link)
            for child_link in child_links:
                print('From child pages:\n', child_link)


if __name__ == "__main__":
    url, recursive = get_url()
    links = get_links(url)
    print_get_links(links, recursive)
