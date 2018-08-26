check-for-hello-world-mesos:
  cmd.run:
    - name: >
        CODE=-1;
        for i in $(seq 1 90);
        do
          curl -s http://localhost:8123/v1/enumerate |
            grep taskmesos-jenkins && CODE=0 && break || (echo fail $i ; sleep 1);
        done;
        test "$CODE" == "0"

check-for-hello-world-marathon:
  cmd.run:
    - name: >
        CODE=-1;
        for i in $(seq 1 90);
        do
          curl -s http://localhost:8123/v1/enumerate |
            grep hello-world.marathon && CODE=0 && break || (echo fail $i ; sleep 1);
        done;
        test "$CODE" == "0"
