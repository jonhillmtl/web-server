import os
import json


class VHostConfigurationNotFoundError(Exception):
    """ the vhosts configuration file can't be found at all """
    vhosts_path = None
    def __init__(self, vhosts_path):
        self.vhosts_path = vhosts_path


class VHostNotFoundError(Exception):
    """ raised if the host can't be found in the specified file """
    host = None
    vhosts_path = None

    def __init__(self, vhosts_path, host):
        self.host = host
        self.vhosts_path = vhosts_path


class VHostConfigurationError(Exception):
    """ raised if the host can be found in the specified file, but is then misconfigured """
    host = None
    vhosts_path = None
    reason = None

    def __init__(self, vhosts_path, host, error):
        self.host = host
        self.vhosts_path = vhosts_path
        self.reason = error


class VHost(object):
    """ represents a virtual host: ie: a hostname mapped to an html_root or wsgi_path """

    # the hostname
    host = None

    # the data associated with that hostname: ie the html_root or wsgi_path, as JSON
    data = None

    # the path to the vhost configuration file, a JSON file
    vhosts_path = None


    def __init__(self, vhosts_path, host):
        self.host = host
        self.vhosts_path = os.path.expanduser(vhosts_path)

        if not os.path.exists(self.vhosts_path):
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

        valid, error = self.validate()
        if valid is False:
            raise VHostConfigurationError(self.vhosts_path, self.host, error)


    def validate(self):
        if self.data is not None:
            if 'html_root' in self.data and 'wsgi_path' in self.data:
                return False, 'html_root and wsgi_path are both present'
        else:
            return False

        return True, ""


    @property
    def html_root(self):
        if self.data is None:
            return None

        html_root = self.data.get('html_root', None)

        if html_root is None:
            return None
        else:
            if os.path.isabs(html_root):
                return html_root
            else:
                return os.path.normpath(os.path.join(os.path.dirname(self.vhosts_path), html_root))


    @property
    def wsgi_path(self):
        # TODO JHILL: support relative paths here! it'll be super important!
        if self.data is None:
            return None
        return self.data.get('wsgi_path', None)


    @property
    def is_wsgi(self):
        return 'wsgi_path' in self.data

