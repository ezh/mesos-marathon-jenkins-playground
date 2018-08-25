jenkins-resources:
  file.recurse:
    - name: /data/jenkins
    - source: salt://resources/data/jenkins

jenkins-config:
  file.managed:
    - name: /data/jenkins/home/config.xml
    - source: salt://resources/data/jenkins/home/config.xml.template
    - template: jinja

jenkins-hello-world-config:
  file.managed:
    - name: /data/jenkins/home/jobs/hello-world-marathon/config.xml
    - source: salt://resources/data/jenkins/home/jobs/hello-world-marathon/config.xml.template
    - template: jinja

jenkins-build:
  cmd.run:
    - name: docker-compose build
    - cwd: /data/jenkins
    - onchanges:
      - jenkins-resources

{% if pillar['start'] is defined %}
jenkins-start:
  cmd.run:
    - name: docker-compose up -d
    - cwd: /data/jenkins
{%endif%}

{% if pillar['stop'] is defined %}
jenkins-stop:
  cmd.run:
    - name: docker-compose stop
    - cwd: /data/jenkins
{%endif%}
