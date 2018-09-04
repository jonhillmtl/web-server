import json
import os
from ..utils import get_parent_paths

class AccessDeniedError(Exception):
    pass


class AccessMalformedError(Exception):
    pass


class Access(object):
    vhost = None
    request = None
    access_data = None
    access_file_path = None

    def __init__(self, vhost, request):
        assert vhost.is_wsgi is False
        self.vhost = vhost
        self.request = request
        self.access_file_path = self._find_access_file()
        self.access_data = []

        if self.access_file_path is not None:
            assert os.path.exists(self.access_file_path)
            with open(self.access_file_path) as f:
                self.access_data = json.loads(f.read())


    def _find_access_file(self):
        html_root = os.path.expanduser(self.vhost.html_root)
        request_path = self.request.path[1:] if self.request.path[0] == '/' else self.request.path
        request_path = os.path.join(html_root, request_path)

        parent_paths = get_parent_paths(request_path, html_root)

        print(parent_paths)
        for pp in parent_paths:
            possible = os.path.join(pp, 'access.json')
            if os.path.exists(possible):
                return possible

        return None


    def get_allowed_ips(self):
        allowed_ips = []
        for ad in self.access_data:
            # TODO JHILL: match path
            if ad['action'] == 'allow' and ad['mode'] == 'from_ip':
                allowed_ips.append(ad['ip'])
        return allowed_ips


    def access(self):
        """
        if len(allow_ips) > 0:
            if 'CLIENT_IP' not in self.request.headers:
                return False

            if not self.request.headers['CLIENT_IP'] in allow_ips:
                return False
        """

        return True