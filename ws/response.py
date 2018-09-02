class Response(object):
    status = None
    content = None

    def __init__(self, status, content):
        self.status = status
        self.content = content


    def __str__(self):
        return "HTTP/1.1 {} Server\n\n{}".format(self.status, self.content)

    @property
    def response(self):
        return str(self).encode('utf-8')