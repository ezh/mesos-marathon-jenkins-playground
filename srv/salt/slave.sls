mesos-slave-resources:
  file.recurse:
    - name: /data/slave
    - source: salt://resources/data/slave

mesos-slave-env:
  file.managed:
    - name: /data/slave/.env
    - source: salt://resources/data/slave/.env.template
    - template: jinja

{% if pillar['start'] is defined %}
mesos-slave-start:
  cmd.run:
    - name: docker-compose up -d
    - cwd: /data/slave
{%endif%}

{% if pillar['stop'] is defined %}
mesos-slave-stop:
  cmd.run:
    - name: docker-compose stop
    - cwd: /data/slave
{%endif%}
