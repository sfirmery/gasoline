# -*- coding: utf-8 -*-

import unittest

from test_api_spaces import SpacesAPITestCase
from test_api_users import UsersAPITestCase
from test_api_comments import CommentsAPITestCase

from tests import suite

if __name__ == '__main__':
    suite.addTest(unittest.makeSuite(UsersAPITestCase))
    suite.addTest(unittest.makeSuite(SpacesAPITestCase))
    suite.addTest(unittest.makeSuite(CommentsAPITestCase))
    unittest.TextTestRunner(verbosity=0).run(suite)
