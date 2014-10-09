# -*- coding: utf-8 -*-

import unittest

from tests import suite as test_suite

if __name__ == '__main__':
    test_suite.setUpSuite()

    # suite = unittest.TestLoader().discover('tests', pattern='test_*.py')
    suite = unittest.TestLoader().discover('tests', pattern='test_api_tags.py')

    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([suite]))
    test_suite.tearDownSuite()
