import json
from urllib.parse import urlparse
import urllib

class Request(object):
    headers_raw = None
    
    headers = None
    method = None
    path = None
    http_version = None
    query_params = None


    def __init__(self, headers_raw):
        self.headers_raw = headers_raw
        self.query_params = dict()
        self.headers = dict()
        self.parse_headers()


    def __str__(self):
        return self.__unicode__()


    def __unicode__(self):
        return """method: {}\nhost: {}\npath: {}\nquery_params: {}\nheaders: {}""".format(
            self.method,
            self.host,
            self.path,
            self.query_params,
            self.headers)


    @property
    def host(self):
        return self.headers['Host'].split(':')[0]


    @property
    def content_length(self):
        return int(self.headers['content-length'].split(':')[0])


    def parse_headers(self):
        print(self.headers_raw)
        lines = self.headers_raw.split('\n\n\n')[0].split('\n')
        self.method, self.path, self.http_version = lines[0].split(' ')

        for line in lines[1:]:
            key = line.split(': ')[0]
            if key != '\r' and key != '':
                if len(line.split(': ')) == 2:
                    self.headers[key] = line.split(': ')[1][:-1]
                else:
                    self.headers[key] = None

        if self.method.lower() == 'get':
            # TODO JHILL: just use someone else's function for this
            query_params = self.path.split('?')
            self.path = query_params[0]

            if len(query_params) == 2:
                self.query_params = urllib.parse.parse_qs(query_params[1])
        else:
            # TODO JHILL: check the content-type here.... just do JSON for now
            json_string = self.headers_raw[-self.content_length:]
            self.query_params = json.loads(json_string)
