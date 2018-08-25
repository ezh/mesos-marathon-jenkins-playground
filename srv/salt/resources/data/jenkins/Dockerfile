FROM jenkins/jenkins:2.138
# if we want to install via apt
USER root
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF
RUN echo deb http://repos.mesosphere.io/ubuntu trusty main > /etc/apt/sources.list.d/mesosphere.list
RUN apt-get update && apt-get install -y software-properties-common apt-transport-https git mesos=1.5.0-2.0.2
RUN wget http://security.debian.org/debian-security/pool/updates/main/o/openssl/libssl1.0.0_1.0.1t-1+deb8u9_amd64.deb
RUN dpkg --install libssl1.0.0_1.0.1t-1+deb8u9_amd64.deb
RUN chsh -s /bin/bash root

COPY plugins.txt /usr/share/jenkins/plugins.txt

RUN /usr/local/bin/install-plugins.sh $(grep -v '#' /usr/share/jenkins/plugins.txt | tr '\n' ' ')
