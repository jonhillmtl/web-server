from nose.tools import *
import unittest
import os
import socket

from . import ServerThread, SocketThread
from ..utils.test import get_fixture_folder

class ServerTestCase(unittest.TestCase):

    def test_basic(self):
        ff = get_fixture_folder()
        vhosts_path = os.path.join(ff, 'vhosts', 'basic', 'vhosts.json')

        st = ServerThread(8045, vhosts_path)
        self.assertNotEqual(st.serversocket, None)
        st.serversocket.close()


    def test_no_socket_available(self):
        ff = get_fixture_folder()
        vhosts_path = os.path.join(ff, 'vhosts', 'basic', 'vhosts.json')

        sockets = []
        for i in range(9000, 9010):
            print(i)
            serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serversocket.bind((socket.gethostname(), i))
            sockets.append(serversocket)

        st = ServerThread(9000, vhosts_path)
        self.assertEqual(st.serversocket, None)

        for s in sockets:
            s.close()


class SocketTestCase(unittest.TestCase):

    def test_basic(self):
        ff = get_fixture_folder()
        vhosts_path = os.path.join(ff, 'vhosts', 'basic', 'vhosts.json')
        socket_thread = SocketThread(None, vhosts_path)

        # TODO JHILL: actually start processing requests here, load them from fixture
