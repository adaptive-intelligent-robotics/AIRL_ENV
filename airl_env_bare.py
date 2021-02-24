#!/usr/bin/env python

"""
AIRL Bare image (no packages installed)
Base Image: ubuntu:18.04
Contents:
   - empty
"""

import hpccm
# Set to 'docker' to generate a Dockerfile or set to 'singularity' to
# generate a Singularity definition file
hpccm.config.set_container_format('singularity')

print(hpccm.primitives.baseimage(image='ubuntu:18.04',_docker_env=False))
print(hpccm.primitives.label(metadata={'Author': 'olle.nilsson19@imperial.ac.uk', 'Version':'v0.1'}))


## ==== Common dependencies ====
print(hpccm.building_blocks.python(python2=False))
print(hpccm.primitives.shell(commands=['ln -s /usr/bin/python3 /usr/bin/python']))


## ==== Composition of building blocks ====
print(hpccm.building_blocks.packages(ospackages=['emacs', 'vim', 'less', 'gdb']))



