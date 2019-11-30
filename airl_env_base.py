#!/usr/bin/env python

"""
AIRL Base image
Contents:
   TBD
"""

import hpccm
from airl_building_blocks import *
# Set to 'docker' to generate a Dockerfile or set to 'singularity' to
# generate a Singularity definition file
hpccm.config.set_container_format('singularity')

print(hpccm.primitives.baseimage(image='ubuntu:18.04',_docker_env=False))
print(hpccm.primitives.label(metadata={'Author': 'a.cully@imperial.ac.uk', 'Version':'v0.2'}))

print(hpccm.building_blocks.python(python2=False))
print(hpccm.primitives.shell(commands=['ln -s /usr/bin/python3 /usr/bin/python']))

#print(hpccm.building_blocks.llvm())
print(hpccm.building_blocks.gnu())

print(hpccm.building_blocks.packages(ospackages=['emacs','vim','less']))

print(hexapod_common())
print(robot_dart())
print(sferes())
print(visu_server())




