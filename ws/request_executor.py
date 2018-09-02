import json
import os


class VHostNotFoundError(Exception):
    vhost = None
    def __init__(self, vhost):
        self.vhost = vhost


class RequestExecutor(object):
    request = None

    def __init__(self, request):
        self.request = request


    def load_vhosts(self):
        path = os.path.expanduser("~/ws/vhosts.json")
        with open(path) as f:
            return json.loads(f.read())


    def execute(self):
        vhosts = self.load_vhosts()
        if self.request.host in vhosts:
            return self.serve_file(vhosts[self.request.host]['path'])
        else:
            raise VHostNotFoundError(self.request.host)


    def serve_file(self, host):
        # TODO JHILL: catch errors, etc...
        host_path = os.path.expanduser(host)
        request_path = self.request.path[1:] if self.request.path[0] == '/' else self.request.path
        filename = os.path.join(host_path, request_path)

        if os.path.isdir(filename):
            filename = os.path.join(filename, 'index.html')

        try:
            with open(filename) as f:
                return f.read()
        except FileNotFoundError as e:
            raise e