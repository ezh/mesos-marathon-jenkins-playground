mesos-master-resources:
  file.recurse:
    - name: /data/master
    - source: salt://resources/data/master

mesos-master-env:
  file.managed:
    - name: /data/master/.env
    - source: salt://resources/data/master/.env.template
    - template: jinja

mesos-master-dns:
  file.managed:
    - name: /data/master/mesosdns/config.json
    - source: salt://resources/data/master/mesosdns/config.json.template
    - template: jinja

mesos-master-build:
  cmd.run:
    - name: docker-compose build
    - cwd: /data/master
    - onchanges:
      - mesos-master-resources

mesos-master-pull:
  cmd.run:
    - name: docker-compose pull zookeeper mesosmaster mesosdns
    - cwd: /data/master
    - onchanges:
      - mesos-master-resources

{% if pillar['start'] is defined %}
mesos-master-start:
  cmd.run:
    - name: docker-compose up -d
    - cwd: /data/master
{%endif%}

{% if pillar['stop'] is defined %}
mesos-master-stop:
  cmd.run:
    - name: docker-compose stop
    - cwd: /data/master
{%endif%}
