mesos-stack:
  file.recurse:
    - name: /data/master
    - source: salt://resources/data/master

mesos-master:
  file.managed:
    - name: /data/master/.env
    - source: salt://resources/data/master-env
    - template: jinja
