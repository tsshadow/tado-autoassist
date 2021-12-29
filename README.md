# tado-autoassist

tado autoassist is based on adrianslabu's tado_aa (https://github.com/adrianslabu/tado_aa/)

I have added docker support, and made username and password settable by commandline. 

The docker image accepts the username and password as environment variables: <br>
`USERNAME`<br>
`PASSWORD`

#Install
The docker image can be build with:
`docker build . -t tag`

The docker image can be started with:
`docker run -e USERNAME=<username> -e PASSWORD=<password>`
