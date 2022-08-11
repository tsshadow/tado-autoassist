#
# tado_autoassist.py
# Created by Teun Schriks <teunschriks@gmail.com> on 29.12.2021
#
# Heavily based on:
# tado_aa.py (Tado Auto-Assist for Geofencing and Open Window Detection)
# Created by Adrian Slabu <adrianslabu@icloud.com> on 11.02.2021
# 

import sys
import time
from huecontrol import *

from datetime import datetime
from PyTado.interface import Tado

def main():
    global lastMessage
    global username
    global password
    global checkingInterval
    global errorRetringInterval
    global enableLog
    global logFile
    lastMessage = ""
    if (len(sys.argv) < 4 ):
        print ("Please set username, password and hue bridge with: python3 <file>.py <username> <password> <ip hue>\n")
    else:
        setup(sys.argv[3]) # hue setup

        username = sys.argv[1] # tado username
        password = sys.argv[2] # tado password

        checkingInterval = 10.0 # checking interval (in seconds)
        errorRetringInterval = 30.0 # retrying interval (in seconds), in case of an error

        enableLog = False # activate the log with "True" or disable it with "False"
        logFile = "/l.log" # log file location

        login()
        t.setDebugging(True)
        homeStatus()
    
def login():

    global t

    try:
        t = Tado(username, password)

        if (lastMessage.find("Connection Error") != -1):
            print ("Connection established, everything looks good now, continuing..\n")

    except KeyboardInterrupt:
        print ("Interrupted by user.")
        sys.exit(0)

    except Exception as e:
        if (str(e).find("access_token") != -1):
            print ("Login error, check the username / password !")
            print ("Username was:"+username)
            sys.exit(0)
        else:
            print (str(e) + "\nConnection Error, retrying in " + str(errorRetringInterval) + " sec..")
            time.sleep(errorRetringInterval)
            login()    

def homeStatus():
    
    global devicesHome

    try:
        homeState = t.getHomeState()["presence"]
        devicesHome = []
        print  (t.getMobileDevices())
        for mobileDevice in t.getMobileDevices():
            if (mobileDevice["settings"]["geoTrackingEnabled"] == True):
                if (mobileDevice["location"] != None):
                    if (mobileDevice["location"]["atHome"]):
                        devicesHome.append(mobileDevice["name"])

        if (lastMessage.find("Connection Error") != -1 or lastMessage.find("Waiting for the device location") != -1):
            print ("Successfully got the location, everything looks good now, continuing..\n")

        if (len(devicesHome) > 0 and homeState == "HOME"):
            if (len(devicesHome) == 1):
                print ("Your home is in HOME Mode, the device " + devicesHome[0] + " is at home.")
            else:
                devices = ""
                for i in range(len(devicesHome)):
                    if (i != len(devicesHome) - 1):
                        devices += devicesHome[i] + ", "
                    else:
                        devices += devicesHome[i]
                print ("Your home is in HOME Mode, the devices " + devices + " are at home.")
        elif (len(devicesHome) == 0 and homeState == "AWAY"):
            print ("Your home is in AWAY Mode and are no devices at home.")
        elif (len(devicesHome) == 0 and homeState == "HOME"):
            print ("Your home is in HOME Mode but are no devices at home.")
            setAway()
        elif (len(devicesHome) > 0 and homeState == "AWAY"):
            if (len(devicesHome) == 1):
                print ("Your home is in AWAY Mode but the device " + devicesHome[0] + " is at home.")
            else:
                devices = ""
                for i in range(len(devicesHome)):
                    if (i != len(devicesHome) - 1):
                        devices += devicesHome[i] + ", "
                    else:
                        devices += devicesHome[i]
                print ("Your home is in AWAY Mode but the devices " + devices + " are at home.")

            setHome()

        devicesHome.clear()
        print ("Waiting for a change in devices location or for an open window..")
        time.sleep(1)
        engine()

    except KeyboardInterrupt:
        print ("Interrupted by user.")
        sys.exit(0)

    except Exception as e:
        if (str(e).find("location") != -1):
            print ("I cannot get the location of one of the devices because the Geofencing is off or the user signed out from tado app.\nWaiting for the device location, until then the Geofencing Assist is NOT active.\nWaiting for an open window..")
            time.sleep(1)
            engine()
        elif (str(e).find("NoneType") != -1):
            time.sleep(1)
            engine()
        else:
            print (str(e) + "\nConnection Error, retrying in " + str(errorRetringInterval) + " sec..")
            time.sleep(errorRetringInterval)
            homeStatus()

def engine():

    i = 0
    while i < 3: # My solution to fix the "stack depth"
        try:
            i = 0
            #Open Window Detection
            for z in t.getZones():
                    zoneID = z["id"]
                    zoneName = z["name"]
                    if (t.getOpenWindowDetected(zoneID)["openWindowDetected"] == True):
                        print (zoneName + ": open window detected, activating the OpenWindow mode.")
                        t.setOpenWindow(zoneID)
                        print ("Done!")
                        print ("Waiting for a change in devices location or for an open window..")
            #Geofencing
            homeState = t.getHomeState()["presence"]

            devicesHome.clear()

            for mobileDevice in t.getMobileDevices():
                if (mobileDevice["settings"]["geoTrackingEnabled"] == True):
                    if (mobileDevice["location"] != None):
                        if (mobileDevice["location"]["atHome"]):
                            devicesHome.append(mobileDevice["name"])

            if (lastMessage.find("Connection Error") != -1 or lastMessage.find("Waiting for the device location") != -1):
                print ("Successfully got the location, everything looks good now, continuing..\n")
                print ("Waiting for a change in devices location or for an open window..")

            if (len(devicesHome) > 0 and homeState == "AWAY"):
                if (len(devicesHome) == 1):
                    print (devicesHome[0] + " is at home, activating HOME mode.")
                else:
                    devices = ""
                    for i in range(len(devicesHome)):
                        if (i != len(devicesHome) - 1):
                            devices += devicesHome[i] + ", "
                        else:
                            devices += devicesHome[i]
                    print (devices + " are at home, activating HOME mode.")
                setHome()
                print ("Done!")
                print ("Waiting for a change in devices location or for an open window..")

            elif (len(devicesHome) == 0 and homeState == "HOME"):
                print ("Are no devices at home")
                setAway()
                print ("Waiting for a change in devices location or for an open window..")

            devicesHome.clear()
            time.sleep(checkingInterval)

        except KeyboardInterrupt:
                print ("Interrupted by user.")
                sys.exit(0)

        except Exception as e:
                if (str(e).find("location") != -1 or str(e).find("NoneType") != -1):
                    print ("I cannot get the location of one of the devices because the Geofencing is off or the user signed out from tado app.\nWaiting for the device location, until then the Geofencing Assist is NOT active.\nWaiting for an open window..")
                    time.sleep(checkingInterval)
                else:
                    print (str(e) + "\nConnection Error, retrying in " + str(errorRetringInterval) + " sec..")
                    time.sleep(errorRetringInterval)

def setAway():
    print ("Activating AWAY mode.")
    t.setAway()
    setAllLightsOn(False) # Turn off ALL hue lights
    print ("Done!")

def setHome():
    print ("Activating HOME mode.")
    t.setHome()
    print ("Done!")

main()
