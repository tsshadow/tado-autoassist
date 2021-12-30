#!/usr/bin/python
from phue import Bridge
bridge = Bridge("192.168.2.1")

def setup():
    bridge = Bridge("192.168.2.1")
    bridge.connect();

def set_all_lights_on(is_on):
    if (is_on):
        print("Turning all lights on")
    else
        print("Turning all lights off")
    lights = bridge.get_light_objects()
    for light in lights:
        light.on = is_on
