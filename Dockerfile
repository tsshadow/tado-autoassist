FROM alpine:3.15.0

ENV USERNAME=
ENV PASSWORD=
RUN apk update &&\
    apk add py3-pip  &&\
    pip3 install python-tado &&\
    pip3 install phue
    
COPY tado_autoassist.py .
COPY huecontrol.py .

ENTRYPOINT python3 tado_autoassist.py ${USERNAME} ${PASSWORD}
