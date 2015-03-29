#!/usr/bin/env python2

import os
import sys
import unittest

from tests.MainTest import MainTestCase

if __name__ == '__main__':

    if not 'TTHA2PASSWORD' in os.environ:
        sys.exit('Password not found')

    suite = unittest.TestSuite((
        unittest.makeSuite(MainTestCase),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())