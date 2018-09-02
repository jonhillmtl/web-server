import threading
import socket
from .response import Response
from .request import Request
from .executors import RequestExecutor
from .executors.base import VHostNotFoundError, InternalServerError
import mimetypes


class SocketThread(threading.Thread):
    clientsocket = None

    def __init__(self, clientsocket):
        super(SocketThread, self).__init__()
        self.clientsocket = clientsocket
        self.start()


    def run(self):
        # TODO JHILL: what if the header is longer than that? or is this too long?
        headers = self.clientsocket.recv(4096).decode()
        request = Request(headers)
        print(request)

        try:
            response = Response(
            status=200,
            content=self.get_content(request),
            content_type=mimetypes.guess_type(request.path)
        )
        except FileNotFoundError as e:
            response = Response(status=404, content=e)
        except VHostNotFoundError as e:
            response = Response(status=404, content=e)
        except InternalServerError as e:
            response = Response(status=500, content=e)
        
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

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((socket.gethostname(), self.port))
        self.serversocket.listen(2)


    def run(self):
        try:
            while self.running:
                print("*" * 100)
                (clientsocket, address) = self.serversocket.accept()
                SocketThread(clientsocket)
        except ConnectionAbortedError:
            pass

    def terminate(self):
        self.serversocket.close()
        self.running = False