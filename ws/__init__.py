import threading
from .server import ServerThread
from argparse import ArgumentParser

argparser = ArgumentParser()
argparser.add_argument('--port', type=int, default=8045, required=False)
args = argparser.parse_args()

def main():
    try:
        server_thread = server.ServerThread(port=args.port)
        server_thread.start()
        server_thread.join()
    except KeyboardInterrupt as e:
        print("\nterminating as cleanly as possible")
        server_thread.terminate()
    except TypeError as e:
        print("\nterminating as cleanly as possible")
        server_thread.terminate()

if __name__ == '__main__':
    main()