

#This is for compatibility with python 3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import serial
import struct
import sys

EditCommands = {
    'estop':        '0x00',
    'stop':         '0x01',
    'pause':        '0x02',
    'resume':       '0x03',
    'run':          '0x04',
    'short_status': '0x07',
    'long_status':  '0x08',
    'version':      '0x0E',
}

RunCommands = {
    'move':         '0x01',
    'home':         '0x02',
    'velocity':     '0x07',
    'vector':       '0x0B',
    'acceleration': '0x0C',
    'configure':    '0x0E',
    'limit_cw':     '0x0F',
    'zero_offset':  '0x13',
    'reset_pos':    '0x15',
}

Motor = {
    'MOTOR_X': 0,
    'MOTOR_Y': 1,
    'MOTOR_Z': 2,
    'MOTOR_W': 3,
    'MOTOR_ALL': 4
}

class GeckoMotion:
    def __init__(self, portName=None):
        self.portname = portName
        
        if self.portname == None:
            self.serialPort = serial.serial_for_url('loop://', timeout = 1)
        else:
            try:
                self.serialPort = serial.Serial(self.portname, 115200, timeout = 1)
                
                if self.serialPort.is_open:
                    self.serialPort.close()
                    
                self.serialPort.open()
            except:
                print("Err 0: Failed to open serial port")
                sys.exit()
        
    
    def __del__(self):
        #FIXME: throws an error when you can't access the serial port
        if not self.portname == None:
            if self.serialPort:
                self.serialPort.close()
    
    def estop(self):
        #FIXME: make it work for all motors
        self._write(self._build_edit_command('estop'))
    
    def get_long_status(self):
        self._write(self._build_edit_command('long_status'))
    
    def get_short_status(self):
        self._write(self._build_edit_command('short_status'))
    
    def home(self, motor):
        #ENHANCE: make home work for MOTOR_ALL
        if motor == 'MOTOR_ALL':
            cmd = self._build_run_command('MOTOR_X', 'home', 0)
            self._test_print(cmd)
        else:
            self._write(self._build_run_command(motor, 'home', 0))
    
    def move(self, motor, distance):
        self._write(self._build_run_command(motor, 'move', distance))
    
    #ENHANCE: consider changing this to a Vector3 input
    #FIXME: put in proper defaults for velocity and acceleration
    def move_to(self, x, y, z, velocity=100, acceleration=50):
        pass
    
    def set_acceleration(self, motor, acceleration):
        self._write(self._build_run_command(motor, 'acceleration', acceleration))
    
    def set_velocity(self, motor, velocity):
        self._write(self._build_run_command(motor, 'velocity', velocity))
    
    def stop(self):
        self._write(self._build_edit_command('stop'))

    '''
    Private Methods
    '''    
    def _build_edit_command(self, command):
        offset = 8
        cmd = int(EditCommands[command], 16) << offset
        cmd = struct.pack('>H', cmd)
        return cmd
        
    def _build_run_command(self, motor, command, data):
        offset = 8
        
        run = struct.pack('<H', int(EditCommands['run'],16))
        cmd = struct.pack('<H', (int(Motor[motor]) << (offset + 6)) + (int(RunCommands[command], 16) << offset) + ((data >> 16) & 0xFF))
        d = data & 0xFFFF
        if data < 0:
            d = struct.pack('<H', abs(data))
        else:
            d = struct.pack('<H', data)
        cmdp = run + cmd + d
        return cmdp
    
    def _read(self):
        msg = self.serialPort.read(self.serialPort.in_waiting)
        #print(':'.join('{:02x}'.format(ord(x)) for x in msg))
        return msg
    
    def _write(self, message):
        self.serialPort.write(message)
    
    '''
    Unit Test Helper Methods
    '''
    def _test_read(self):
        ret = self.serialPort.readline()
        value = ' '.join('{:02x}'.format(ord(x)) for x in ret)
        return value
    
    def _test_print(self, hexData):
        print(':'.join('{:02x}'.format(ord(x)) for x in hexData))
        