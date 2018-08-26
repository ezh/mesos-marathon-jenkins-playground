run-hello-world-mesos:
  cmd.run:
    - name: curl -v -X POST {{pillar['jenkins']['url']}}/job/hello-world-mesos/build --user $JENKINS_AUTH
    - env:
      - JENKINS_AUTH: {{pillar['jenkins']['auth']}}

run-hello-world-marathon:
  cmd.run:
    - name: curl -v -X POST {{pillar['jenkins']['url']}}/job/hello-world-marathon/build --user $JENKINS_AUTH
    - env:
      - JENKINS_AUTH: {{pillar['jenkins']['auth']}}
