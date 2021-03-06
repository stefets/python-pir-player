#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import logging
import os
import time
import subprocess
from gpiozero import MotionSensor
from datetime import datetime

log = logging.getLogger(__name__)

class MotionLogic:

    def __init__(self, pin):

        self.Sensor = MotionSensor(pin)
        self.ProcPlayer = None

    def Dispose(self):
        del self.Sensor

    # Sensor -----------------------------------------
    def StartSensor(self):
        self.Sensor.when_motion = self.OnMotionStart
        self.Sensor.when_no_motion = self.OnMotionStop

    # Sensor Events
    def OnMotionStart(self):
        print "OnMotionStart"
        log.info("OnMotionStart") 
        print self.ProcPlayer
        if self.ProcPlayer is None:
            self.ProcPlayer = subprocess.Popen(['omxplayer', '-o', 'local', 'video.avi'])
        elif self.ProcPlayer.poll() is not None:
            self.ProcPlayer = subprocess.Popen(['omxplayer', '-o', 'local', 'video.avi'])

    def OnMotionStop(self):
        print "OnMotionStop "
        log.info("OnMotionStop")
        if self.ProcPlayer is not None:
            print self.ProcPlayer.poll()

##################################################################################################################################################

def main(args=None):

    logging.basicConfig(filename='debug-player.log',datefmt='%Y-%m-%d %I:%M:%S',format='%(levelname)s : %(asctime)s %(message)s',level=logging.DEBUG)

    logic = MotionLogic(7)
    logic.StartSensor()
 
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt):
        print('exit(0)')
    finally:
        logic.Dispose()
        del logic
        log.info("Shutdown")
        sys.exit()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
