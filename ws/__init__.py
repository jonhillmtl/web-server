import threading
from .server import ServerThread
from argparse import ArgumentParser
import subprocess

argparser = ArgumentParser()
argparser.add_argument('--http_port', type=int, default=8045, required=False)
argparser.add_argument('--https_port', type=int, default=8065, required=False)
argparser.add_argument('--vhosts_path', type=str, default='~/ws/vhosts.json')
args = argparser.parse_args()


def main():
    try:
        http_thread = server.ServerThread(port=args.http_port, vhosts_path=args.vhosts_path, secure=False)
        http_thread.start()
        subprocess.check_call(["open", "http://{}:{}/".format(
            http_thread.host,
            http_thread.port)]
        )

        https_thread = server.ServerThread(port=args.https_port, vhosts_path=args.vhosts_path, secure=True)
        https_thread.start()
        if https_thread.serversocket is not None:
            subprocess.check_call(["open", "https://{}:{}/".format(
                https_thread.host,
                https_thread.port)]
            )
        
        http_thread.join()
        https_thread.join()
    except KeyboardInterrupt as e:
        print("\nterminating as cleanly as possible")
        http_thread.terminate()
        https_thread.terminate()
    except TypeError as e:
        print(e)
        print("\nterminating as cleanly as possible")
        http_thread.terminate()
        https_thread.terminate()

if __name__ == '__main__':
    main()