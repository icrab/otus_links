from urlparser import parser

if __name__ == '__main__':
    log = parser.start_logging()
    url, recursive = parser.get_url(log)
    links = parser.get_links(url, recursive, log)
    parser.print_recieved_links(links, recursive, log)

