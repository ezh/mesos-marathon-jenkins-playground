/data:
  file.directory:
    - makedirs: True

docker:
  pkg.installed:
    - name: docker
  service.running:
    - enable: True
    - reload: True
    - require:
      - pkg: docker

docker-compose:
  pip.installed:
    - name: docker-compose

