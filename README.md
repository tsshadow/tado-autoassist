# tado-autoassist (Tado Auto-Assist for Geofencing and Open Window Detection)
A python script that automatically adjusts the temperature in your home at leaving or arriving based on your settings from tado app and automatically switch off the heating (activating Open Window Mode) in the room where tado TRV detects an open window.
tado autoassist is based on adrianslabu's tado_aa (https://github.com/adrianslabu/tado_aa/)

##tado-autoassist adds the following:
The docker image accepts the username and password as environment variables: <br>
`USERNAME`<br>
`PASSWORD`

#Install
The docker image can be build with:
`docker build . -t tag`

The docker image can be started with:
`docker run -e USERNAME=<username> -e PASSWORD=<password>`
