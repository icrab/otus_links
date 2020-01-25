from urlparser import parser

if __name__ == '__main__':
    log_path = 'logs/log'
    log = parser.Log(log_path)
    request = parser.Request(log)
    urls = parser.Urls(request, log)
    urls.print()

