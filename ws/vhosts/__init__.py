import os
import json


class VHostNotFoundError(Exception):
    vhost = None
    def __init__(self, vhost):
        self.vhost = vhost


class VHost(object):
    host = None
    data = None

    def __init__(self, vhosts_path, host):
        self.host = host

        # TODO JHILL: load the vhosts file
        self.data = json.loads(open(os.path.expanduser(vhosts_path)).read())[self.host]

    @property
    def exists(self):
        # TODO JHILL
        return True

    @property
    def html_root(self):
        if self.exists:
            return self.data['html_root']
        return None


    @property
    def wsgi_path(self):
        if self.exists:
            return self.data['wsgi_path']
        return None

    @property
    def is_wsgi(self):
        if self.exists:
            return 'wsgi_path' in self.data
        return False
