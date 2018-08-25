FROM mesosphere/marathon:v1.7.50

RUN apt-get update
RUN apt-get install -y curl
RUN curl -sLf https://github.com/karlkfi/probe/releases/download/v0.3.0/probe-0.3.0-linux_amd64.tgz | tar zxf - -C /usr/local/bin/
