import unittest
import testingtools
from testingtools import load_save
import krpc

class TestVessel(testingtools.TestCase):

    def test_basic(self):
        load_save('flight')
        ksp = krpc.connect()
        vtype = ksp.space_center.VesselType
        vsituation = ksp.space_center.VesselSituation
        vessel = ksp.space_center.active_vessel

        self.assertEqual('Test', vessel.name)
        vessel.name = 'Foo Bar Baz';
        self.assertEqual('Foo Bar Baz', vessel.name)

        self.assertEqual(vtype.ship, vessel.type)
        vessel.type = vtype.station
        self.assertEqual(vtype.station, vessel.type)

        self.assertEqual(vsituation.orbiting, vessel.situation)

if __name__ == "__main__":
    unittest.main()
