AIRL_environment
============



# The AIRL_env containers

The AIRL_env container can be found [here](https://cloud.sylabs.io/library/_container/5d14ffc961e2655558b3b082#container-top)
Several versions are available. 

The base version contains:
- [Sferes2](https://github.com/sferes2/sferes2), a lightweight, generic C++11 framework for evolutionary computation
- [Dart](https://dartsim.github.io/), Dynamic Animation and Robotics Toolkit, a physical simulator used to simulate our robots. 
- [Robot_Dart](https://github.com/resibots/robot_dart), a generic wrapper around the DART simulator.

The tensorflow version extends the base version with:
- [Tensorflow](https://www.tensorflow.org/), compiled from source with cuda 10 and ready to link with sferes2. 
