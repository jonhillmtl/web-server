from nose.tools import *
import unittest
import os

from . import Access, AccessDeniedError, AccessMalformedError
from ..utils.test import get_fixture_folder
from ..http.request import Request
from ..vhosts import VHost

class AccessTestCase(unittest.TestCase):

    def test_find_access_file_in_parent(self):
        ff = get_fixture_folder()
        vhosts_path = os.path.join(ff, 'access', 'basic', 'vhosts.json')
        raw_request = open(os.path.join(ff, 'requests', 'access_abc.txt')).read()
        mock_request = Request(raw_request)
        self.assertNotEqual(mock_request, None)

        vhost = VHost(vhosts_path, mock_request.host)
        self.assertNotEqual(vhost, None)

        access = Access(vhost, mock_request)
        self.assertEqual('access/basic/a/access.json', access.access_file_path[len(ff) + 1:])


    def test_find_access_file_for_html_file(self):
        ff = get_fixture_folder()
        vhosts_path = os.path.join(ff, 'access', 'basic', 'vhosts.json')
        raw_request = open(os.path.join(ff, 'requests', 'access_abc_static.txt')).read()
        mock_request = Request(raw_request)
        self.assertNotEqual(mock_request, None)

        vhost = VHost(vhosts_path, mock_request.host)
        self.assertNotEqual(vhost, None)

        access = Access(vhost, mock_request)
        self.assertEqual('access/basic/a/access.json', access.access_file_path[len(ff) + 1:])


    def _test_validation_invalid(self, invalid_subdir):
        ff = get_fixture_folder()
        vhosts_path = os.path.join(ff, 'access', 'validation', 'invalid', invalid_subdir, 'vhosts.json')
        raw_request = open(os.path.join(ff, 'requests', 'basic.txt')).read()
        mock_request = Request(raw_request)
        self.assertNotEqual(mock_request, None)

        vhost = VHost(vhosts_path, mock_request.host)
        self.assertNotEqual(vhost, None)

        access = Access(vhost, mock_request)


    def test_validation_invalid(self):
        with self.assertRaises(AccessMalformedError) as context:
            self._test_validation_invalid('001')
        self.assertEquals(context.exception.error, 'access rule must contain action')

        with self.assertRaises(AccessMalformedError)  as context:
            self._test_validation_invalid('002')
        self.assertEquals(context.exception.error, 'access rule must contain mode')

        with self.assertRaises(AccessMalformedError) as context:
            self._test_validation_invalid('003')
        self.assertEquals(context.exception.error, "invalid not in ['allow', 'deny']")

        with self.assertRaises(AccessMalformedError) as context:
            self._test_validation_invalid('004')
        self.assertEquals(context.exception.error, "from not in ['from_ip']")
        