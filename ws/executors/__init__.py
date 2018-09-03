import json
import os

from .base import WsgiExecutableNotImplementedError
from .static import StaticRequestExecutor
from .wsgi_python import WsgiPythonRequestExecutor
from .wsgi_php import WsgiPhpRequestExecutor
from ..access import Access, AccessDeniedError
from ..vhosts import VHost, VHostNotFoundError


class RequestExecutor(object):
    request = None
    vhosts_path = None

    def __init__(self, request, vhosts_path):
        self.request = request
        self.vhosts_path = vhosts_path


    def execute(self):
        vhost = VHost(self.vhosts_path, self.request.host)
        # TODO JHILL: throw different errors here...
        if vhost.validate is False:
            raise VHostNotFoundError()

        executor = None

        # TODO JHILL: is this the best place to be checking access?
        # this is the only time we know the vhost...
        access = Access(vhost, self.request)
        if not access.access():
            raise AccessDeniedError()

        if vhost.is_wsgi:
            wsgi_executable = vhost.wsgi_path.split('/')[-1].split(".")[1]

            if wsgi_executable == 'py':
                executor = WsgiPythonRequestExecutor(vhost, self.request)
            elif wsgi_executable == 'php':
                executor = WsgiPhpRequestExecutor(vhost, self.request)
            else:
                raise WsgiExecutableNotImplementedError(wsgi_executable)
        else:
            executor = StaticRequestExecutor(vhost, self.request)

        return executor.serve()
