import mimetypes
import socket
import threading


from ..access import Access, AccessDeniedError
from ..executors import RequestExecutor
from ..executors.base import InternalServerError
from ..vhosts import VHostNotFoundError
from ..http.request import Request
from ..http.response import Response


class SocketThread(threading.Thread):
    clientsocket = None
    vhosts_path = None


    def __init__(self, clientsocket, vhosts_path):
        super(SocketThread, self).__init__()
        self.vhosts_path = vhosts_path
        self.clientsocket = clientsocket


    def run(self):
        # TODO JHILL: what if the header is longer than that? or is this too long?
        request_text = self.clientsocket.recv(4096).decode()

        self.process_request(request_text)

        self.clientsocket.send(response.response)
        self.clientsocket.close()


    def process_request(self, request_text):
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


    def get_content(self, request):
        request_executor = RequestExecutor(request, self.vhosts_path)
        return request_executor.execute()


class ServerThread(threading.Thread):
    port = None
    serversocket = None
    running = True
    host = None
    vhosts_path = None

    def __init__(self, port, vhosts_path):
        super(ServerThread, self).__init__()
        self.port = port
        self.vhosts_path = vhosts_path

        while self.port < port + 10:
            try:
                self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.serversocket.bind((socket.gethostname(), self.port))
                self.serversocket.listen(2)

                self.host = socket.gethostname()
                break
            except OSError:
                self.serversocket = None
                self.port = self.port + 1


        # TODO JHILL: maybe we didn't get a socket, raise an error!

        print("connected on port: {}".format(self.port))
        print("connected on host: {}".format(self.host))


    def run(self):
        try:
            while self.running:
                print("*" * 100)
                (clientsocket, address) = self.serversocket.accept()
                st = SocketThread(clientsocket, self.vhosts_path)
                st.start()
        except ConnectionAbortedError:
            pass


    def terminate(self):
        self.serversocket.close()
        self.running = False