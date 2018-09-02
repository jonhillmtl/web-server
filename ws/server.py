import threading
import socket
from .response import Response
from .request import Request
from .request_executor import RequestExecutor, VHostNotFoundError

MSGLEN = 80

class SocketThread(threading.Thread):
    clientsocket = None

    def __init__(self, clientsocket):
        super(SocketThread, self).__init__()
        self.clientsocket = clientsocket
        self.start()


    def run(self):
        headers = self.clientsocket.recv(4096).decode()
        request = Request(headers)
        print(request)

        try:
            response = Response(status=200, content=self.get_content(request))
        except FileNotFoundError:
            response = Response(status=404, content='file not found on server')
        except VHostNotFoundError:
            response = Response(status=404, content='vhost not found')

        self.clientsocket.send(response.response)
        self.clientsocket.close()


    def get_content(self, request):
        request_executor = RequestExecutor(request)
        return request_executor.execute()


class ServerThread(threading.Thread):
    port = None
    sock = None

    def __init__(self, port):
        super(ServerThread, self).__init__()
        self.port = port

        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((socket.gethostname(), self.port))
        serversocket.listen(2)
        self.sock = serversocket

    def run(self):
        while True:
            print("*" * 100)
            (clientsocket, address) = self.sock.accept()
            SocketThread(clientsocket)
