""" dart building block"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import posixpath

import hpccm.config
import hpccm.templates.git
import hpccm.templates.rm



from hpccm.building_blocks.base import bb_base
from hpccm.building_blocks.pip import pip

from hpccm.primitives.comment import comment
from hpccm.primitives.workdir import workdir
from hpccm.primitives.shell import shell
from hpccm.building_blocks.packages import packages


class qdax(bb_base, hpccm.templates.git, hpccm.templates.rm):

    def __init__(self, **kwargs):
        """Initialize building block"""

        super(qdax, self).__init__(**kwargs)

        self.__ospackages = kwargs.get('ospackages', [ 
                                                      'cmake',
                                                      'g++',
                                                      'ffmpeg',
                                                      'xvfb',
                                                      'git',
                                                      'python3-pip',
                                                      'python3-dev',
                                                      ])
        self.__commands = []  # Filled in by __setup()
        self.__wd = '/git'  # working directory

        # Construct the series of steps to execute
        self.__setup()

        # Fill in container instructions
        self.__instructions()

    def __instructions(self):
        """Fill in container instructions"""

        self += comment('====INSTALLING QDax====')
        self += packages(ospackages=self.__ospackages)

        self += shell(commands=self.__commands)
        self += pip(packages=['jax==0.4.7', 'jaxlib==0.4.7+cuda12_cudnn88 -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html'], pip='pip3')
        
        self += comment('====DONE QDax====')

    def __setup(self):
        """Construct the series of shell commands, i.e., fill in
           self.__commands"""
        ...
        # Clone source
        path_qdax = posixpath.join(self.__wd, 'QDax')

        # Configure, Install and Cleanup
        self.__commands.append(self.clone_step(branch='v0.2.2',
                                               repository='https://github.com/adaptive-intelligent-robotics/QDax.git',
                                               path=self.__wd,
                                               directory='QDax')
                               )
        self.__commands.append(f"cd {self.__wd}/QDax/")
        self.__commands.append("pip3 install -r requirements.txt")
        self.__commands.append(self.cleanup_step([path_qdax]))


