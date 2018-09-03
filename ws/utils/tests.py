from nose.tools import *
import unittest
import os

from . import get_parent_paths
from .test import get_fixture_folder

class UtilsTestCase(unittest.TestCase):

    def test_fixture_folder(self):
        self.assertNotEquals(get_fixture_folder(), None)


    def test_parent_paths(self):
        ff = get_fixture_folder()
        child_path = os.path.join(ff, 'parent_paths/a/b/c/')
        stop_at = os.path.join(ff, 'parent_paths')

        self.assertTrue(os.path.exists(child_path))

        self.assertEquals(
            get_parent_paths(child_path, stop_at),
            [
                os.path.join(ff, 'parent_paths/a/b/c'),
                os.path.join(ff, 'parent_paths/a/b'),
                os.path.join(ff, 'parent_paths/a'),
                os.path.join(ff, 'parent_paths')
            ]
        )
        