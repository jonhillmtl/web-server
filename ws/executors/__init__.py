import json
import os

from .static import StaticRequestExecutor
from .wsgi_python import WsgiPythonRequestExecutor
from .wsgi_php import WsgiPhpRequestExecutor


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
            executor = None
            vhost = vhosts[self.request.host]

            if 'wsgi_path' in vhost:
                wsgi_executable = vhost['wsgi_path'].split('/')[-1].split(".")[1]

                if wsgi_executable == 'py':
                    executor = WsgiPythonRequestExecutor(vhost, self.request)
                elif wsgi_executable == 'php':
                    executor = WsgiPhpRequestExecutor(vhost, self.request)
                else:
                    raise WsgiExecutableNotImplementedError(wsgi_executable)
            else:
                executor = StaticRequestExecutor(vhost, self.request)

            return executor.serve()
        else:
            raise VHostNotFoundError(self.request.host)
