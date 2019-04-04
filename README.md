
AIRL_env
============

AIRL_env is a [docker](https://docs.docker.com/) environment which includes most of the tools commonly used in the AIRL Lab. 
It includes:
- [Sferes2](https://github.com/sferes2/sferes2), a lightweight, generic C++11 framework for evolutionary computation
- [Dart](https://dartsim.github.io/), Dynamic Animation and Robotics Toolkit, a physical simulator used to simulate our robots. 
- [Robot_Dart](https://github.com/resibots/robot_dart), a generic wrapper around the DART simulator.
- (TO COME) [Tensorflow](https://www.tensorflow.org/), compiled from source with cuda 10 and ready to link with sferes2. 

# Using AIRL_env
-----------
## Install docker
First you need to have Docker installed, more information [here](https://docs.docker.com/install/), or for Ubuntu specifically [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/). We will assume in the following that your are on the docker groups as suggested [here](https://docs.docker.com/install/linux/linux-postinstall/), and the commands will not be prefaced with "sudo". 

## Pull the docker image
To pull the docker image you can run the following command: 
```
docker pull aneoshun/airl_env:dart_exp_ready
```
Note: `dart_exp_ready` refers to the current latest tag, to check the other and future tags have a look [here](https://hub.docker.com/r/aneoshun/airl_env/tags).

You can check that the image has been downloaded with the following command: 
```
docker image ls
```
which should return something like: 
```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
aneoshun/airl_env   dart_exp_ready      ee1dda2b4673        17 hours ago        4.56GB
```

## Start a docker container from the docker image
Now that the image has been downloaded, we can start to use it. 
A `start_container.sh` is provided in this repository, which provides an easy way to start a container from the AIRL_env image. This script first checks if a container using the AIRL_env has already been created and use this one, or otherwise creates one. 

The name of the image (and its tag) can be changed at the beginning of the script. 

So, to launch the container, simply run `./start_container.sh`, which should directly give you access to a terminal prompt like this: 
`root@0dac1511ca98:/git# ` 

You are inside the virtual environment of the Docker container. You can do most of the things you will normally do in the ubuntu terminal (cd, ls, etc..). You can quit it with `exit` or ctrl+c. If you want to re-join the container, simply run again `./start_container.sh`

Be careful, if you delete the container (via `docker rm XXXXXX` where XXXXX is the container ID) all the changes you made in the virtual environment will be lost. 