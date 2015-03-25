#!/usr/bin/env python2

import sys
import unittest

from tests.MyTest import MyTestCase

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(MyTestCase),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())