class Response(object):
    status = None
    content = None
    content_type =  None

    def __init__(self, status, content, content_type):
        self.status = status
        self.content = content
        self.content_type = content_type

    @property
    def content_length(self):
        return len(self.content)

    def __str__(self):
        # TODO JHILL: mime types, pngs aren't transferring
        return """HTTP/1.1 {} Server
Content-Length: {}
Content-Type: {}


{}
        """.format(
            self.status,
            self.content_length,
            self.content_type,
            self.content
        )

    @property
    def response(self):
        return str(self).encode('utf-8')