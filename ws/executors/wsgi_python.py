import os
import importlib.util

from .base import BaseRequestExecutor


class WsgiPythonRequestExecutor(BaseRequestExecutor):
    def serve(self):
        try:
            wsgi_path = os.path.expanduser(self.vhost['wsgi_path'])
            spec = importlib.util.spec_from_file_location("wsgi", wsgi_path)
            wsgi = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(wsgi)
            return wsgi.execute(self.request)

        except FileNotFoundError as e:
            raise InternalServerError(e)
        except Exception as e:
            raise InternalServerError(e)