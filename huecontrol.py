#!/usr/bin/python
from phue import Bridge
import time
import sys

#global object
bridge = None

def setup(ip):
    global bridge
    result = False
    while result is False:
        try:
            # connect
            time.sleep(5)
            print("Connecting to bridge ("+ip+")... press the button on the hue switch")
            bridge = Bridge(ip)
            bridge.connect()
            result = True
        except KeyboardInterrupt:
            print ("Interrupted by user.")
            sys.exit(0)
        except:
            pass # try again
    print("Succesfully logged in")


def setAllLightsOn(is_on):
    global bridge
    print("Turning all lights on" if is_on else "Turning all lights off")
    lights = bridge.get_light_objects()
    for light in lights:
        light.on = is_on

