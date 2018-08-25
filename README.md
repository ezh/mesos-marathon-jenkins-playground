# mesos-marathon-jenkins-playground
Deploy mesos-marathon-jenkins-playground with SaltStack

SaltStack, docker-compose + a bit of python.
Deploying environment as root with private key /path/to/private/ssh/key/id_rsa

```
python deploy.py --priv=~/path/to/private/ssh/key/id_rsa --masters=1.1.1.1,1.1.1.2 --slaves=1.1.1.2,1.1.1.3 --jenkins=1.1.1.1 -l info
```

* 1.1.1.1 - only master node + Jenkins
* 1.1.1.2 - master + slave node
* 1.1.1.3 - only slave node

After deployment there will be:
* 1.1.1.1:5050 - Mesos
* 1.1.1.1:8080 - Marathon
* 1.1.1.1:8081 - Jenkins
------
* 1.1.1.2:5050 - Mesos
* 1.1.1.2:8051 - Slave
* 1.1.1.2:8080 - Marathon
------
* 1.1.1.3:8051 - Slave

Alexey Aksenov, 2018 MIT license
