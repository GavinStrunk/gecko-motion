import unittest
from GeckoMotion import GeckoMotion

class TestGeckoMotion(unittest.TestCase):
    
    def setUp(self):
        self.gecko = GeckoMotion()
            
    def test_setup(self):
        self.assertTrue(True)

    def test_fakeSerialLoopbackSetup(self):
        gecko = GeckoMotion()
    
    def test_eStopXMotor(self):
        self.gecko.estop()
        self.assertEquals('00 00', self.gecko._test_read())
        
    def test_stopXMotor(self):
        self.gecko.stop()
        self.assertEquals('01 00', self.gecko._test_read())
    
    def test_xAcceleration(self):
        self.gecko.set_acceleration('MOTOR_X', 100)
        self.assertEquals('04 00 00 0c 64 00', self.gecko._test_read())
    
    def test_xVelocity(self):
        self.gecko.set_velocity('MOTOR_X', 500)
        self.assertEquals('04 00 00 07 f4 01', self.gecko._test_read())
    
    def test_xMovePositiveDirection(self):
        self.gecko.move('MOTOR_X', 10000)
        self.assertEquals('04 00 00 01 10 27', self.gecko._test_read())
        
    def test_xQueryShortStatus(self):
        self.gecko.get_short_status()
        self.assertEquals('07 00', self.gecko._test_read())
    
    def test_xQueryLongStatus(self):
        self.gecko.get_long_status()
        self.assertEquals('08 00', self.gecko._test_read())
        
    def test_xHome(self):
        self.gecko.home('MOTOR_X')
        self.assertEquals('04 00 00 02 00 00', self.gecko._test_read())
        
    def test_yVelocity(self):
        self.gecko.set_velocity('MOTOR_Y', 500)
        self.assertEquals('04 00 00 47 f4 01', self.gecko._test_read())
        
    def test_yAcceleration(self):
        self.gecko.set_acceleration('MOTOR_Y', 100)
        self.assertEquals('04 00 00 4c 64 00', self.gecko._test_read())
        
    def test_yMovePositionDirection(self):
        self.gecko.move('MOTOR_Y', 10000)
        self.assertEquals('04 00 00 41 10 27', self.gecko._test_read())
        
    def test_yQueryShortStatus(self):
        self.gecko.get_short_status()
        self.assertEquals('07 00', self.gecko._test_read())
    
    def test_xyzHome(self):
        self.gecko.home('MOTOR_ALL')
        self.assertEquals('04 00 00 22 00 00', self.gecko._test_read())
        
if __name__ == '__main__':
    unittest.main()
    