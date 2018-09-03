import json
import os


class AccessDeniedError(Exception):
    pass


class Access(object):
    vhost = None
    request = None
    access_data = None

    def __init__(self, vhost, request):
        self.vhost = vhost
        self.request = request

        # TODO JHILL: figure out how to do individual files

        html_root = os.path.expanduser(self.vhost.html_root)
        request_path = self.request.path[1:] if self.request.path[0] == '/' else self.request.path
        access_path = os.path.join(html_root, request_path, 'access.json')

        if not os.path.exists(access_path):
            self.access_data = list()
        else:
            with open(access_path) as f:
                self.access_data = json.loads(f.read())


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