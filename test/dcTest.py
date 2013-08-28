'''
Created on Aug 21, 2013

@author: arkilic
'''
import unittest
from pyBL.Config import config


class Test(unittest.TestCase):


    def setUp(self):
        config(name='test', geometry='sixcircle', engine='you', tag='default', author='arman')

    def tearDown(self):
        pass


    def testConfig(self):
        
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()