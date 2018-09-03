import os
import json


class VHostConfigurationNotFoundError(Exception):
    vhosts_path = None
    def __init__(self, vhosts_path):
        self.vhosts_path = vhosts_path


class VHostNotFoundError(Exception):
    host = None
    vhosts_path = None

    def __init__(self, vhosts_path, host):
        self.host = host
        self.vhosts_path = vhosts_path


class VHostConfigurationError(Exception):
    host = None
    vhosts_path = None
    reason = None

    def __init__(self, vhosts_path, host, reason):
        self.host = host
        self.vhosts_path = vhosts_path
        self.reason = reason


class VHost(object):
    host = None
    data = None
    vhosts_path = None


    def __init__(self, vhosts_path, host):
        self.host = host
        self.vhosts_path = os.path.expanduser(vhosts_path)

        if not os.path.exists(vhosts_path):
            raise VHostConfigurationNotFoundError(vhosts_path)
        else:
            try:
                data = json.loads(open(self.vhosts_path).read())
            except json.decoder.JSONDecodeError as e:
                raise VHostConfigurationError(self.vhosts_path, self.host, str(e))

            # TODO JHILL: lowercase all the host keys

            if self.host not in data:
                raise VHostNotFoundError(self.vhosts_path, self.host)
            else:
                self.data = data[self.host]

        if self.validate is False:
            raise VHostConfigurationError(self.vhosts, self.host)


    @property
    def validate(self):
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
