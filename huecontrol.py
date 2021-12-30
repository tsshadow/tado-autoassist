#!/usr/bin/python
from phue import Bridge
import time
import sys

def setup(ip):
    result = False
    while result is False:
        try:
            # connect
            time.sleep(5)
            print("Connecting to bridge ("+ip+")... press the button on the hue switch")
            bridge = Bridge(ip)
            bridge.connect()
        except KeyboardInterrupt:
            print ("Interrupted by user.")
            sys.exit(0)
        except:
            pass # try again

def set_all_lights_on(is_on):
    print("Turning all lights" + "on" if is_on else "off")
    lights = bridge.get_light_objects()
    for light in lights:
        light.on = is_on

