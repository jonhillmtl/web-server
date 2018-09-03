import mimetypes
import socket
import threading


from ..access import Access, AccessDeniedError
from ..executors import RequestExecutor
from ..executors.base import VHostNotFoundError, InternalServerError
from ..http.request import Request
from ..http.response import Response


class SocketThread(threading.Thread):
    clientsocket = None

    def __init__(self, clientsocket):
        super(SocketThread, self).__init__()
        self.clientsocket = clientsocket
        self.start()


    def run(self):
        # TODO JHILL: what if the header is longer than that? or is this too long?
        request_text = self.clientsocket.recv(4096).decode()
        request = Request(request_text)
        request.headers['CLIENT_IP'] = self.clientsocket.getsockname()[0]
        print(request)

        try:
            response = Response(
                status=200,
                content=self.get_content(request),
                content_type=mimetypes.guess_type(request.path)
            )
        except FileNotFoundError as e:
            response = Response(status=404, content=str(e), content_type='')
        except VHostNotFoundError as e:
            response = Response(status=404, content=str(e), content_type='')
        except InternalServerError as e:
            response = Response(status=500, content=str(e), content_type='')
        except AccessDeniedError as e:
            response = Response(status=401, content=str(e), content_type='')

        self.clientsocket.send(response.response)
        self.clientsocket.close()


    def get_content(self, request):
        request_executor = RequestExecutor(request)
        return request_executor.execute()


class ServerThread(threading.Thread):
    port = None
    serversocket = None
    running = True

    def __init__(self, port):
        super(ServerThread, self).__init__()
        self.port = port

        while True:
            try:
                self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.serversocket.bind((socket.gethostname(), self.port))
                self.serversocket.listen(2)
                break
            except OSError:
                self.port = self.port + 1

        print("connected on port: {}".format(self.port))
        print("connected on host: {}".format(socket.gethostname()))


    def run(self):
        try:
            while self.running:
                print("*" * 100)
                (clientsocket, address) = self.serversocket.accept()
                print(clientsocket)
                SocketThread(clientsocket)
        except ConnectionAbortedError:
            pass


    def terminate(self):
        self.serversocket.close()
        self.running = False