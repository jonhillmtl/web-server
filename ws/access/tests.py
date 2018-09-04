from nose.tools import *
import unittest
import os

from . import Access
from ..utils.test import get_fixture_folder
from ..http.request import Request
from ..vhosts import VHost

class AccessTestCase(unittest.TestCase):

    def test_find_access_file_in_parent(self):
        ff = get_fixture_folder()
        vhosts_path = os.path.join(ff, 'access', 'vhosts.json')
        raw_request = open(os.path.join(ff, 'requests', 'access_abc.txt')).read()
        mock_request = Request(raw_request)
        self.assertNotEqual(mock_request, None)

        vhost = VHost(vhosts_path, mock_request.host)
        self.assertNotEqual(vhost, None)

        access = Access(vhost, mock_request)
        self.assertEqual('access/a/access.json', access.access_file_path[len(ff) + 1:])


    def test_find_access_file_for_html_file(self):
        ff = get_fixture_folder()
        vhosts_path = os.path.join(ff, 'access', 'vhosts.json')
        raw_request = open(os.path.join(ff, 'requests', 'access_abc_static.txt')).read()
        mock_request = Request(raw_request)
        self.assertNotEqual(mock_request, None)

        vhost = VHost(vhosts_path, mock_request.host)
        self.assertNotEqual(vhost, None)

        access = Access(vhost, mock_request)
        self.assertEqual('access/a/access.json', access.access_file_path[len(ff) + 1:])