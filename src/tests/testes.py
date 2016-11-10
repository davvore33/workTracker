import unittest

from Events import Events
from invoice_creator import invoice_creator


class invoice_test(unittest.TestCase):
    def test_invoice_creator(self):
        self.events = [
            Events(date="11/09/2001", duration="4", description="", client="Federico Scarpa", key="123", payed=False)]
        tex = invoice_creator("/home/matteo/Documenti/workTracker", self.events, "Federico Scarpa")
        if tex.write():
            self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
