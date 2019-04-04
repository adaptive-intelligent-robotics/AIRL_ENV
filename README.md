
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
## Pull the docker image
First you need to have Docker installed, more information [here](https://docs.docker.com/install/), or for Ubuntu specifically [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/). We will assume in the following that your are on the docker groups as suggested [here](https://docs.docker.com/install/linux/linux-postinstall/), and the commands will not be prefaced with "sudo". 
