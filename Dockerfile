FROM alpine:3.15.0

ENV USERNAME=
ENV PASSWORD=
ENV IP_HUE=
RUN apk update &&\
    apk add py3-pip  &&\
    apk add git &&\
    pip3 install git+https://github.com/wmalgadey/PyTado.git &&\
    pip3 install phue 
    
COPY tado_autoassist.py .
COPY huecontrol.py .

ENTRYPOINT python3 tado_autoassist.py ${USERNAME} ${PASSWORD} ${IP_HUE}
