import os
from .base import BaseRequestExecutor


class StaticRequestExecutor(BaseRequestExecutor):
    def serve(self):
        html_root = os.path.expanduser(self.vhost['html_root'])
        request_path = self.request.path[1:] if self.request.path[0] == '/' else self.request.path
        filename = os.path.join(html_root, request_path)

        if os.path.isdir(filename):
            filename = os.path.join(filename, 'index.html')
        try:
            # TODO JHILL: try this some other way?
            if '.png' in filename:
                with open(filename, "rb") as f:
                    return f.read()
            else:
                with open(filename) as f:
                    return f.read()
        except FileNotFoundError as e:
            raise e
