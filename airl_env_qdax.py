#!/usr/bin/env python

"""
AIRL BRAX/JAX image
Base Image: nvidia/cuda:11.4.2-cudnn8-devel-ubuntu20.04
Contents:
   - 
"""

import hpccm
from hpccm.building_blocks.pip import pip

from airl_building_blocks import *

# Set to 'docker' to generate a Dockerfile or set to 'singularity' to
# generate a Singularity definition file
hpccm.config.set_container_format('singularity')

print(hpccm.primitives.baseimage(image='nvidia/cuda:12.0.1-cudnn8-devel-ubuntu20.04', _docker_env=False))
print(hpccm.primitives.label(metadata={'Author': 'luca.grillotti16@imperial.ac.uk', 'Version': 'v1.0'}))

## ==== Common dependencies ====
print(hpccm.building_blocks.python(python2=False, devel=True))
print(hpccm.primitives.shell(commands=['ln -s /usr/bin/python3 /usr/bin/python']))

# print(hpccm.building_blocks.llvm())
print(hpccm.building_blocks.gnu())

## ==== Composition of building blocks ====
print(hpccm.building_blocks.packages(ospackages=['emacs', 'vim', 'less', 'gdb']))

#  print(hexapod_common())
print(visu_server())
print(brax())

