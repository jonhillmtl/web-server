class Request(object):
    headers = None

    action = None
    path = None
    http_version = None
    host = None
    query_params = None

    def __init__(self, headers):
        self.headers = headers
        self.query_params = dict()

        self.parse_headers()

    def __unicode__(self):
        return """
host: {}
        
        """.format(self.host)

    def parse_headers(self):
        print(self.headers)
        print("-" * 20)
        lines = self.headers.split('\n')
        self.action, self.path, self.http_version = lines[0].split(' ')

        for line in lines:
            if line.startswith('Host:'):
                self.host = line.split(' ')[1].split(":")[0]

        query_params = self.path.split('?')
        if len(query_params) == 2:
            query_params = query_params[1]
            for qp in query_params.split('&'):
                qp_split = qp.split('=')
                self.query_params[qp_split[0]] = qp_split[1]
            print(self.query_params)