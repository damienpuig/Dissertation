import unittest
from ServicesTest.valueservicetest import ValueServiceTest

def AllTests():

	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(ValueServiceTest))

	return suite

if __name__ == '__main__':
	unittest.TextTestRunner(verbosity=2).run(AllTests())