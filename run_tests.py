#!/usr/bin/env python2

import os
import sys
import unittest

from tests.test_auth import AuthTestCase
from tests.test_topic import CreateTopicTestCase, RemoveTopicTestCase

if __name__ == '__main__':

    if not 'TTHA2PASSWORD' in os.environ:
        sys.exit('Password not found')

    suite = unittest.TestSuite((
        # unittest.makeSuite(AuthTestCase),
        # unittest.makeSuite(CreateTopicTestCase),
        # unittest.makeSuite(RemoveTopicTestCase)
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())