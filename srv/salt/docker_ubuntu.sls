/data:
  file.directory:
    - makedirs: True

docker-support:
  pkg.installed:
    - name: linux-image-extra-virtual

docker-repo:
  pkgrepo.managed:
    - humanname: Docker repo
    - name: deb [arch=amd64] https://download.docker.com/linux/ubuntu trusty stable
    - file: /etc/apt/sources.list.d/docker.list
    - keyid: 0EBFCD88
    - keyserver: keyserver.ubuntu.com
    - require:
      - pkg: docker-support

docker:
  pkg.installed:
    - name: docker-ce
    - require:
      - pkgrepo: docker-repo
  service.running:
    - enable: True
    - reload: True
    - require:
      - pkg: docker

docker-compose:
  pip.installed:
    - name: docker-compose
