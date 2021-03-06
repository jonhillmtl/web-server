from ..utils.test import get_fixture_folder
from ..vhosts import VHost, VHostConfigurationNotFoundError, VHostConfigurationError

from nose.tools import *

import os
import unittest


class VHostsTestCase(unittest.TestCase):

    def test_basic(self):
        ff = get_fixture_folder()
        vhosts_path = os.path.join(ff, 'vhosts', 'basic', 'vhosts.json')

        vhost = VHost(vhosts_path, 'jons-mbp.fritz.box')
        self.assertNotEqual(vhost, None)


    def test_vhost_configuration_not_found(self):
        ff = get_fixture_folder()
        vhosts_path = os.path.join(ff, 'vhosts', 'not_found.json')

        with self.assertRaises(VHostConfigurationNotFoundError) as context:
            vhost = VHost(vhosts_path, '')


    def test_malformed_json(self):
        ff = get_fixture_folder()
        vhosts_path = os.path.join(ff, 'vhosts', 'invalid', 'malformed_json.json')

        with self.assertRaises(VHostConfigurationError) as context:
            vhost = VHost(vhosts_path, '')


    def test_html_wsgi_both_present(self):
        ff = get_fixture_folder()
        vhosts_path = os.path.join(ff, 'vhosts', 'html_wsgi_both_present', 'vhosts.json')

        with self.assertRaises(VHostConfigurationError) as context:
            vhost = VHost(vhosts_path, 'jons-mbp.fritz.box')
            
        