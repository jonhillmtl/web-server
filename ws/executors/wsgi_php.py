import os
import subprocess


from .base import BaseRequestExecutor, InternalServerError


class WsgiPhpRequestExecutor(BaseRequestExecutor):
    def serve(self):
        try:
            wsgi_path = os.path.expanduser(self.vhost['wsgi_path'])
            return subprocess.check_output(["php", wsgi_path]).decode()
        except FileNotFoundError as e:
            print(e)
            raise InternalServerError(e)
        except Exception as e:
            print(e)
            raise InternalServerError(e)