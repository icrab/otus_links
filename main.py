from urlparser import parser

if __name__ == '__main__':
    url, recursive = parser.get_url()
    links = parser.get_links(url, recursive)
    parser.print_get_links(links, recursive)

