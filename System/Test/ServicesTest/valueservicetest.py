import unittest
from Services.valueservice import ValueService
from Objects.device import Device

class ValueServiceTest(unittest.TestCase):

    def setUp(self):
        self.valueservice = ValueService()

    def test_getValuesByDevice(self):
        # make sure the shuffled sequence does not lose any elements
        device = Device(name='arduino1', description='lalala')
        limit = 5

        current = self.valueservice.getValuesByDevice(device, limit)

        self.assertEqual(current.isvalid, False)