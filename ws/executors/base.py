class VHostNotFoundError(Exception):
    vhost = None
    def __init__(self, vhost):
        self.vhost = vhost


class InternalServerError(Exception):
    process = None
    def __init__(self, process):
        self.process = process


class WsgiExecutableNotImplementedError(Exception):
    executable = None
    def __init__(self, executable):
        self.executable = executable



class BaseRequestExecutor(object):
    vhost = None
    request = None

    def __init__(self, vhost, request):
        self.vhost = vhost
        self.request = request
