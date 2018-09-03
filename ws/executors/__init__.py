import json
import os

from .base import WsgiExecutableNotImplementedError
from .static import StaticRequestExecutor
from .wsgi_python import WsgiPythonRequestExecutor
from .wsgi_php import WsgiPhpRequestExecutor
from ..access import Access, AccessDeniedError

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
        if self.request.host.lower() in vhosts:
            executor = None
            
            # TODO JHILL: the hosts aren't necessarily in the vhosts in lower case,
            # should we lowercase them here?
            vhost = vhosts[self.request.host.lower()]

            # TODO JHILL: is this the best place to be checking access?
            # this is the only time we know the vhost...
            access = Access(vhost, self.request)
            if not access.access():
                raise AccessDeniedError()

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
