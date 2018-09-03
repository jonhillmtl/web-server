import threading
from .server import ServerThread
from argparse import ArgumentParser
import subprocess

argparser = ArgumentParser()
argparser.add_argument('--port', type=int, default=8045, required=False)
argparser.add_argument('--vhosts_path', type=str, default='~/ws/vhosts.json')
args = argparser.parse_args()

def main():
    try:
        server_thread = server.ServerThread(port=args.port, vhosts_path=args.vhosts_path)
        server_thread.start()
        subprocess.check_call(["open", "http://{}:{}/".format(
            server_thread.host,
            server_thread.port)]
        )
        server_thread.join()
    except KeyboardInterrupt as e:
        print("\nterminating as cleanly as possible")
        server_thread.terminate()
    except TypeError as e:
        print(e)
        print("\nterminating as cleanly as possible")
        server_thread.terminate()

if __name__ == '__main__':
    main()