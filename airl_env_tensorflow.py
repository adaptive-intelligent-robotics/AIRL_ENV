#!/usr/bin/env python

"""
AIRL Tensorflow image
Base Image: nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04
Contents:
   - hexapod
   - robot_dart
   - sferes
   - visu_server
   - tensorflow
"""

import hpccm
from airl_building_blocks import *
# Set to 'docker' to generate a Dockerfile or set to 'singularity' to
# generate a Singularity definition file
hpccm.config.set_container_format('singularity')

print(hpccm.primitives.baseimage(image='nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04',_docker_env=False))
print(hpccm.primitives.label(metadata={'Author': 'a.cully@imperial.ac.uk', 'Version':'v0.2'}))


## ==== Common dependencies ====
print(hpccm.building_blocks.python(python2=False,devel=True))
print(hpccm.primitives.shell(commands=['ln -s /usr/bin/python3 /usr/bin/python']))

#print(hpccm.building_blocks.llvm())
print(hpccm.building_blocks.gnu())


## ==== Composition of building blocks ====
print(hpccm.building_blocks.packages(ospackages=['emacs', 'vim', 'less', 'gdb']))

print(hexapod_common())
print(robot_dart(simd = False))
print(sferes(simd = False))
print(visu_server())
print(tensorflow(simd = False)) # The simd is not used for now on TF building block





