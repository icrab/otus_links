import logging
import requests
import re
import os.path
from bs4 import BeautifulSoup
from requests.exceptions import Timeout


class Log():
    '''Class for logging'''
    def __init__(self, path):
        '''Init takes log file path'''
        if not os.path.exists(path):
            try:
               create_file = open(path, 'w')
            except Exception:
                print('failed to create logfile')
                exit()

            create_file.close()

        logging.basicConfig(filename=path, level=logging.INFO)
        self.log = logging.getLogger('urlparser')

    def print_and_logging_exception(self, *args):
        '''Method for outputs and write exceptions to log'''
        self.log.exception(args[0])
        print(', '.join(args))


class Request():
    '''Class to request setup'''
    google = 'https://www.google.com/search?q='
    yandex = 'https://yandex.ru/search/?text='

    def __init__(self, log):
        '''Init takes log file and gets search query'''
        self.__log = log
        print('Enter search query:')
        self.__request = str(input())
        self.__site = self.__choose_site()
        self.recursive = self.__recursive_search()
        self.url = self.__site + self.__request


    def __key_controls(self, message):
        '''Method to control keyboard input'''
        key = 0

        while key != 1 and key != 2:
            print(message)
            try:
                key = int(input())
                if key == 3: exit()
            except ValueError:
                self.__log.print_and_logging_exception('ValueError')
            except KeyboardInterrupt:
                self.__log.print_and_logging_exception('KeyboardInterrupt', 'for exit press 3')

        if key == 1: return True
        else: return False


    def __choose_site(self):
        '''Method to selection search site'''
        message = 'Press 1 for search in google.com or 2 for search in ya.ru. 3 for exit'
        choosen_site = self.__key_controls(message)

        if choosen_site:
            site = self.google
        else:
            site = self.yandex 

        return site


    def __recursive_search(self):
        '''Method to verify that recursion is requied'''
        message = 'Press 1 if you need recursive search or 2 if not. 3 for exit'
        recursive = self.__key_controls(message)

        return recursive


class Urls():
    '''Class to getting, processing and print urls'''
    def __init__(self, request, log):
        self.__log = log
        self.links = self.get_links(request.url, request.recursive)

    def get_links(self, url, recursive):
        '''Method to gets links'''
        links = []

        try:
            page = requests.get(url, timeout=5).text
        except requests.exceptions.ConnectionError:
            self.__log.print_and_logging_exception('ConnectionError')
            return links
        except Timeout:
            self.__log.print_and_logging_exception('Timeout')
            return links
        except Exception:
            self.__log.print_and_logging_exception('OtherTrouble')
            return links

        links = self.__processing_links(page, links)

        if not recursive:
            return links
        else:
            child_links = []
            for link in links:
                for child in self.get_links(link, False):
                    child_links.append(child)

        return links + child_links

    def __processing_links(self, page, links):
        '''Method to processing links'''
        dirty_links = []

        soup = BeautifulSoup(page, 'html.parser')

        for link in soup.find_all('a', href=True):
            dirty_links.append(link['href'])

        for dirty_link in dirty_links:
            dirty_link = re.sub(r'^.*http', 'http' , dirty_link)
            if re.match(r'(http|https)://', dirty_link) is not None:
                links.append(dirty_link)

        return links


    def __get_number_of_links(self, links):
        '''Method to  get number of links'''
        number_of_links = len(self.links) 
        input_number_of_links = 0

        print(f'Found {len(links)} links. Enter numbers of links to display:')
        while input_number_of_links == 0:
            try: 
                input_number_of_links = int(input())
                if number_of_links < input_number_of_links:
                    input_number_of_links = 0
                    print(f'Entered number more then {number_of_links}, try again:')
            except ValueError:
                self.__log.print_and_logging_exception('ValueError', 'Need number')

        return input_number_of_links


    def print(self):
        '''Method to print links'''
        input_number_of_links = self.__get_number_of_links(self.links)

        for i,link in enumerate(self.links):
            if i < input_number_of_links:
                print(i+1,'-',link)


