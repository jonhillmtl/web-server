import threading
from .server import ServerThread
from argparse import ArgumentParser

argparser = ArgumentParser()
argparser.add_argument('--port', type=int, default=8045, required=False)
args = argparser.parse_args()

def main():
    server_thread = server.ServerThread(port=args.port)
    server_thread.start()
    server_thread.join()

if __name__ == '__main__':
    main()