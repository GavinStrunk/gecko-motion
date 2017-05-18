'''
You need to make sure you have access to the serial port before running
'''
from GeckoMotion import GeckoMotion
import time

def demo1(gecko):
    gecko.set_acceleration('MOTOR_X', 100)
    gecko.set_velocity('MOTOR_X', 500)
    
    print("Move X motor")
    gecko.move('MOTOR_X', 15000)
    
    time.sleep(1)
    gecko.get_short_status()
    print("Stop Motor after done")
    gecko.stop()
    
    #print("Send E Stop")
    #gecko.estop('MOTOR_X')
    
def demo2(gecko):
    #print("Get drive status")
    gecko.get_long_status()
    time.sleep(0.02)
    msg = gecko._read()
    gecko._test_print(msg)
    
def demo3(gecko):
    gecko.set_acceleration('MOTOR_Y', 100)
    gecko.set_velocity('MOTOR_Y', 500)
    print("Move Y motor")
    gecko.move('MOTOR_Y', 5000)
    gecko.get_short_status()

def demo4(gecko):
    gecko.set_acceleration('MOTOR_X', 100)
    gecko.set_velocity('MOTOR_X', 500)
    print("Move x motor home")
    gecko.home('MOTOR_X')

if __name__ == '__main__':
    
    print("Start Gecko Motion Demo Program")
    gecko = GeckoMotion('/dev/ttyUSB0')
    
    demo1(gecko)
    #for i in range(100):
    #    demo2(gecko)
    #demo3(gecko)
    #demo4(gecko)
    print("Demo completed")
    pass