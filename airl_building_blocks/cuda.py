""" Torch building block"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import hpccm.templates.git
from hpccm.building_blocks.base import bb_base
from hpccm.building_blocks.conda import conda
from hpccm.building_blocks.packages import packages
from hpccm.primitives.comment import comment
from hpccm.primitives.environment import environment
from hpccm.primitives.shell import shell


class torch(bb_base, hpccm.templates.git):
    def __init__(self, **kwargs):
        """Initialize building block"""

        super(torch, self).__init__(**kwargs)

        self.__ospackages = kwargs.get('ospackages', ['ca-certificates',
                                                      'git',
                                                      'curl',
                                                      'libcurl3-dev',
                                                      'libfreetype6-dev',
                                                      'libhdf5-serial-dev',
                                                      'libzmq3-dev',
                                                      'libtool',
                                                      'rsync',
                                                      'software-properties-common',
                                                      'unzip',
                                                      'autoconf',
                                                      'automake',
                                                      'zip',
                                                      'zlib1g-dev'])

        self.__simd = kwargs.get('simd', True)
        self.__workspace = kwargs.get('workspace', '/workspace')
        # self.__cuda_version = kwargs.get('cuda_version', '10.1')
        # self.__cudnn_version = kwargs.get('cudnn_version', '7')
        self.__anaconda_path = kwargs.get('anaconda_path', '/usr/local/anaconda')
        self.__max_jobs = kwargs.get('max_jobs', 16)

        self.__commands = []  # Filled in by __setup()
        self.__tests = []  # Filled in by __setup()
        self.__wd = '/git'  # working directory

        # Construct the series of steps to execute
        self.__setup()

        # Fill in container instructions
        self.__instructions()

    def __instructions(self):
        """Fill in container instructions"""

        self += comment('====INSTALLING Torch=====')
        self += packages(ospackages=self.__ospackages)
        self += conda(packages=['numpy',
                                'ninja',
                                'pyyaml',
                                'mkl',
                                'mkl-include',
                                'setuptools',
                                'cmake',
                                'cffi',
                                'typing_extensions',
                                'future',
                                'six',
                                'requests',
                                'dataclasses',
                                'magma-cuda111'],
                      channels=['pytorch'],
                      eula=True)

        self += environment(variables={'LD_LIBRARY_PATH': f'{self.__workspace}/lib/torch/:$LD_LIBRARY_PATH'})

        self += shell(commands=self.__commands)
        self += shell(commands=self.__tests, _test=True)
        self += comment('====DONE TORCH=====')

    def __setup_torch(self):
        self.__commands.append(f"mkdir -p {self.__wd}")
        self.__commands.append(f"cd {self.__wd}")

        # Install Torch
        self.__commands.append("git clone --recursive https://github.com/pytorch/pytorch --branch v1.8.0")
        self.__commands.append("cd pytorch")
        self.__commands.append('export CMAKE_PREFIX_PATH=${CONDA_PREFIX:-"$(dirname $(which conda))/../"}')
        self.__commands.append(f'MAX_JOBS={self.__max_jobs} python setup.py install')

        # Create symlinks from workspace to torch include and lib
        torch_path = f'{self.__anaconda_path}/lib/python3.7/site-packages/torch'

        self.__commands.append(f'mkdir -p {self.__workspace}/lib')
        self.__commands.append(f'ln -s {torch_path}/lib     {self.__workspace}/lib/torch')

        self.__commands.append(f'mkdir -p {self.__workspace}/include')
        self.__commands.append(f'ln -s {torch_path}/include {self.__workspace}/include/torch')

    def __cleanup(self):
        self.__commands.append(f"cd {self.__wd}")
        self.__commands.append(f"rm -rf {self.__wd}/pytorch")

    def __setup(self):
        """Construct the series of shell commands, i.e., fill in
           self.__commands"""
        self.__setup_torch()
        self.__cleanup()
