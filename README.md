
AIRL_env
============

AIRL_env is a [docker](https://docs.docker.com/) environment which includes most of the tools commonly used in the AIRL Lab. 
It includes:
- [Sferes2](https://github.com/sferes2/sferes2), a lightweight, generic C++11 framework for evolutionary computation
- [Dart](https://dartsim.github.io/), Dynamic Animation and Robotics Toolkit, a physical simulator used to simulate our robots. 
- [Robot_Dart](https://github.com/resibots/robot_dart), a generic wrapper around the DART simulator.
- (TO COME) [Tensorflow](https://www.tensorflow.org/), compiled from source with cuda 10 and ready to link with sferes2. 

# Using AIRL_env
## Install docker
First you need to have Docker installed, more information [here](https://docs.docker.com/install/), or for Ubuntu specifically [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/). We will assume in the following that your are on the docker groups as suggested [here](https://docs.docker.com/install/linux/linux-postinstall/), and the commands will not be prefaced with "sudo". 

## Pull the docker image
To pull the docker image you can run the following command: 
```
docker pull aneoshun/airl_env:latest
```
You can check that the image has been downloaded with the following command: 
```
docker image ls
```
which should return something like: 
```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
aneoshun/airl_env   latest              5b47d0ae7998        15 minutes ago      4.77GB
```

## Start a docker container from the docker image
Now that the image has been downloaded, we can start to use it. 
A `start_container.sh` is provided in this repository, which provides an easy way to start a container from the AIRL_env image. This script first checks if a container using the AIRL_env has already been created and use this one, or otherwise creates one. 
```
If using Cygwin or MINGW on Windows:
- it may be needed to escape $LOCAL_EXP_PATH passed in docker run arguments with a single backslash to bind mount correctly
- docker commands may have to be prefixed with winpty to run
```
The name of the image (and its tag) can be changed at the beginning of the script. 

So, to launch the container, simply run `./start_container.sh`, which should directly give you access to a terminal prompt like this: 
`root@0dac1511ca98:/git# ` 

You are inside the virtual environment of the Docker container. You can do most of the things you will normally do in the ubuntu terminal (cd, ls, etc..). You can quit it with `exit` or ctrl+c. If you want to re-join the container, simply run again `./start_container.sh`

Be careful, if you delete the container (via `docker rm XXXXXX` where XXXXX is the container ID) all the changes you made in the virtual environment will be lost. 

## Add Sferes2 experiments and run them
### Adding experiments
 Sferes2 is a framework designed for research purposes. Therefore, it is articulated around "experiments". Each experiment has its own folder in the `sferes2/exp` folder. Most of the code you will write/edit/run will be located in one of these subfolders. Of course, you don't want to risk loosing all your code if for some reason you delete your Docker container. Therefore, we made the `sferes2/exp` folder point to a folder on your host system (your local OSX or linux machine). This way, you can locally edit your code with your favorite IDE, without the need to go through the Docker virtual environment. 

Because most of our experiments are also stored on a git repository (if you don't store your code on a git server, like github or gitlab, I *strongly* encourage you do to so), we made the `start_container.sh` script link the `sferes2/exp` folder to the `~/git` folder by default (this can be changed in the `start_container.sh` script). This way, all the folders contained in the `~/git` folder on your local machine can be used as Sferes2 experiments. 

**example_dart_exp** is an example of Sferes2 experiment available [here](https://gitlab.doc.ic.ac.uk/AIRL/example_dart_exp). 
We can clone it in our local git folder: 
```
cd ~/git
git clone git@gitlab.doc.ic.ac.uk:AIRL/example_dart_exp.git
```
if we start the container, we can now see it listed in the `sferes/exp` folder (among other folders):
```
antoine@aion:~/git/airl_env$ ./start_container.sh 
root@0dac1511ca98:/git# ls sferes2/exp/
airl_env  example_dart_exp
```

### Configuring and compiling Sferes2
Sferes should be configured and compiled via the `./waf configure` and `./waf` commands. However, these commands will not conpile your experiments. To properly configure and compile your experiment you should tell waf to specifically consider them. For instance, to compile the example_dart_exp experiment:
First log on the container with `./start_container.sh`, then go to the `sferes2` folder: `cd sferes2/`, from there, you can configure sferes with this command: 
```
./waf configure --exp example_dart_exp/ --dart /workspace --robot_dart /workspace
```
This command has three parts. First, `./waf configure` means that we want to configure the build process. Then, ` --exp example_dart_exp/` says that we want to include our experiment in the configuration process. This will load all the configuration options and files associated with this experiment. Lastly, `--dart /workspace --robot_dart /workspace` are two options (`--dart` and `--robot_dart`) which specify to waf where it can find the include and library files for the Dart and robot_dart libraries. On the Docker image, all the libraries are installed in the /workspace/ folder (this is designed to enable an easier exportation on a system where sudo rights are not available). 

After running the configuration command you should obtain something like this:
```
Command-line options for exp [exp/example_dart_exp] : /git/sferes2/exp/example_dart_exp/waf_tools
Hi her
 -> OK 
Setting top to                           : /git/sferes2 
Setting out to                           : /git/sferes2/build 
Checking for 'g++' (C++ compiler)        : /usr/bin/g++ 
Checking boost includes                  : 1_65_1 
Checking boost libs                      : ok 
Checking Intel TBB includes (optional)   : /usr/include 
Checking Intel TBB libs (optional)       : /usr/lib/x86_64-linux-gnu 
Checking for MPI include (optional)      : ok 
Checking for MPI libs (optional)         : Not found 
Checking for Eigen                       : ok 
Checking for ssrc kdtree (KD-tree)       : Not found 
Configuring for exp [example_dart_exp/]
conf exp:
Hi hllkjer
Checking for DART includes (including io/urdf) : ok 
Checking for DART gui includes                 : Not found 
DART: Checking for optional Bullet includes    : ok 
Checking for DART libs (including io/urdf)     : ok 
DART: Checking for Assimp                      : ok 
Checking for DART gui libs                     : Not found 
Checking for robot_dart includes               : ok 
Checking for robot_dart libs                   : ok 
done
example_dart_exp/ -> ok

--- configuration ---
compiler(s):
 * CXX: gcc
boost version: 1_65_1
mpi: False
Compilation flags :
   CXXFLAGS : -D_REENTRANT -Wall -fPIC -ftemplate-depth-1024 -Wno-sign-compare -Wno-deprecated  -Wno-unused -DSFERES_ROOT="/git/sferes2"  -std=c++11 -DEIGEN3_ENABLED 
   LINKFLAGS: 
--- license ---
Sferes2 is distributed under the CECILL license (GPL-compatible)
Please check the accompagnying COPYING file or http://www.cecill.info/
'configure' finished successfully (0.082s)
```
We can in particular see that the Dart library is found (except for the GUI elements which are current disabled on purpose). 

Now that the configuration is completed, we can compile our experiment: 
```
./waf --exp example_dart_exp
```
which should lead to: 
```
Command-line options for exp [exp/example_dart_exp] : /git/sferes2/exp/example_dart_exp/waf_tools
Hi her
 -> OK 
Waf: Entering directory `/git/sferes2/build'
DEBUG is is disabled
Entering directory `/git/sferes2'
Building exp: example_dart_exp
[14/15] Compiling exp/example_dart_exp/dart_exp.cpp
In file included from ../exp/example_dart_exp/dart_exp.cpp:49:0:
/git/sferes2/sferes/qd/container/archive.hpp:275:2: warning: #warning "No KD_TREE library found: no qd/container/archive.hpp" [-Wcpp]
 #warning "No KD_TREE library found: no qd/container/archive.hpp"
  ^~~~~~~
In file included from /git/sferes2/sferes/misc/rand.hpp:47:0,
                 from /git/sferes2/sferes/misc.hpp:41,
                 from /git/sferes2/sferes/gen/evo_float.hpp:47,
                 from ../exp/example_dart_exp/dart_exp.cpp:38:
/git/sferes2/sferes/misc/rand_utils.hpp:436:25: warning: mangled name for 'static uint32_t randutils::auto_seeded<SeedSeq>::hash(T&&) [with T = void (*)(int) throw (); SeedSeq = randutils::seed_seq_fe<4, unsigned int>]' will change in C++17 because the exception specification is part of a function type [-Wnoexcept-type]
         static uint32_t hash(T&& value)
                         ^~~~
/git/sferes2/sferes/misc/rand_utils.hpp:436:25: warning: mangled name for 'static uint32_t randutils::auto_seeded<SeedSeq>::hash(T&&) [with T = std::chrono::time_point<std::chrono::_V2::system_clock, std::chrono::duration<long int, std::ratio<1, 1000000000> > > (*)() noexcept; SeedSeq = randutils::seed_seq_fe<4, unsigned int>]' will change in C++17 because the exception specification is part of a function type [-Wnoexcept-type]

[15/15] Linking build/exp/example_dart_exp/example
Waf: Leaving directory `/git/sferes2/build'
'build' finished successfully (14.226s)
```
 The experiment is now compiled and ready to run!
 To run it simply call the executable: 
 `build/exp/example_dart_exp/example`
 which will print something like this after a couple of time: 
 ```
 root@0dac1511ca98:/git/sferes2# build/exp/example_dart_exp/example
INIT Robot
End init Robot
writing...archive_0
writing...progress
2019-04-04_12_05_39_207/gen_0 written
```
This experiment can run for a LONG period of time, so you will probably want to kill it with ctrl+c.

Sferes2 creates a new folder for execution of the experiments. For instance, in the example above, the folder `2019-04-04_12_05_39_207` contains all the file produced during the experiment. These files are precious and they are the experimental data that you will use to analyse the performance of the algorithms. You will have to extract these file from the Docker container. This can be done by copying them in your experiment's folder. (NOTE: this currently does not work on the AIRL Computing server because of the NFS rights managements, can be solved my mounting a volume on the local hard drive).


# Enabling graphical interfaces 

For a cross-platform visualisation of the opengl environment, we use in combination xinit (Xdummy), x11vnc, and novnc, to setup a HTML5 viewer that shows a direct stream of the container's graphical interface. 
To start the visualisation server (VISU_server), simply type in the container’s terminal:
```
root@0dac1511ca98:/git# visu_server.sh&
```
This command will start the different processes and the graphical interface can be seen on any modern web browser. If you are running the docker container locally, you can access to the interface at the address [http://localhost:6081/](http://localhost:6081/) (the IP can be changed in the start_container.sh).
You can test the interface by going into the robot_dart folder and running one of the example:
```
root@0dac1511ca98:/git# cd robot_dart/
root@0dac1511ca98:/git/robot_dart# ./build/tutorial
```
You should see on the viewer’s webpage the result of the physical simulation (in this example: a set of boxes and spheres falling on a robotic arm).
You can shutdown the visu_server by putting its process forward (`fg`) and killing it with a ctrl+c. 

