tengu-cli
=========

*Tengu command line program in Python.*


Purpose
-------

This is a Tengu cli program used to simplify application deployments.


Usage
-----

If you've cloned this project, and want to install the library (*and all
development dependencies*), the command you'll want to run is::

    $ pip install -e .

Before using the cli, make sure you are logged into docker.
```
docker login
```
The docker command must be usable without `sudo`. Make sure the docker socket on the host machine has sufficient permissions.
```
ubuntu@juju-c41e8b-35:~$ ll /var/run/docker.sock
srw-rw-rw- 1 root docker 0 Nov 28 10:43 /var/run/docker.sock=
```
The Tengu cli will use port `5000` to push deployments to the deployer api.
