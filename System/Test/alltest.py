import unittest
from ServicesTest.valueservicetest import ValueServiceTest

#We started to implement a test procedure, but
#it appeared that we didn't finish it
#due to lack of time.
def AllTests():

	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(ValueServiceTest))

	return suite

if __name__ == '__main__':
	unittest.TextTestRunner(verbosity=2).run(AllTests())