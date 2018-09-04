import json
from urllib.parse import urlparse
import urllib

class Request(object):
    request_raw = None

    headers = None

    # GET, POST, PUT, DELETE
    method = None

    path = None
    http_version = None
    query_params = None


    def __init__(self, request_raw):
        self.request_raw = request_raw
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
        # the content will be split from the header information by three newlines,
        # the one at the end of the content and two for blank lines,
        # so if we split it there we can separate them cleanly for parsing
        lines = self.request_raw.split('\n\n\n')[0].split('\n')

        try:
            self.method, self.path, self.http_version = lines[0].split(' ')
        except ValueError:
            print(lines[0])
            # TODO JHILL: probably bail here, the request is probably
            # hopelessly malformed if that didn't work

        # TODO JHILL: make sure that the method is acceptable, ie: in a list of
        # methods that we can deal with

        # skip throught the lines and break them apart on ': ' to get
        # a dictionary of key value pairs
        # start from the second line because the first was consumed above
        for line in lines[1:]:
            key = line.split(': ')[0]

            # these two show up for some reason
            if key != '\r' and key != '':
                if len(line.split(': ')) == 2:
                    self.headers[key] = line.split(': ')[1][:-1]
                else:
                    self.headers[key] = None


        # parse out the query_params or content of the request
        if self.method.lower() == 'get':
            # TODO JHILL: just use someone else's function for this
            query_params = self.path.split('?')
            self.path = query_params[0]

            if len(query_params) == 2:
                self.query_params = urllib.parse.parse_qs(query_params[1])
        else:
            # TODO JHILL: check the content-type here.... just do JSON for now
            json_string = self.request_raw[-self.content_length:]
            self.query_params = json.loads(json_string)
