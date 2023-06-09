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


class brax(bb_base, hpccm.templates.git, hpccm.templates.rm):

    def __init__(self, **kwargs):
        """Initialize building block"""

        super(brax, self).__init__(**kwargs)

        self.__ospackages = kwargs.get('ospackages', [ 
                                                      'cmake',
                                                      'ffmpeg',
                                                      'xvfb',
                                                      'git',
                                                      'python3-pip',
                                                     ])
        self.__commands = [] # Filled in by __setup()
        self.__wd = '/git' # working directory

        # Construct the series of steps to execute
        self.__setup()

        # Fill in container instructions
        self.__instructions()

    def __instructions(self):
        """Fill in container instructions"""

        self += comment('====INSTALLING BRAX====')
        self += packages(ospackages=self.__ospackages)
        self += pip(packages=['absl-py==1.0.0',
                              'jax==0.3.10',
                              'brax==0.0.12',
                              'dm-haiku==0.0.5',
                              'flax==0.4.1',
                              'gym==0.23.1',
                              'ipython',
                              'jupyter',
                              'numpy==1.22.3',
                              'protobuf==3.19.4',
                              'scikit-learn==1.0.2',
                              'scipy==1.8.0',
                              'seaborn==0.11.2',
                              'sklearn==0.0',
                              'tensorflow-probability==0.15.0',
                              'typing-extensions==3.10',
                              'hydra-core==1.1.2',
                              'tk==0.1.0',
                              'pre-commit==2.12.1',
                              'pytest==6.2.5',
                              'pytest-assume==2.4.3',
                              ], 
                              pip='pip3')
        self += pip(packages=['jaxlib==0.3.10+cuda11_cudnn82 -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html'], pip='pip3')
        self += shell(commands=self.__commands)
        
        self += comment('====DONE BRAX====')

    def __setup(self):
        """Construct the series of shell commands, i.e., fill in
           self.__commands"""

        # Clone source
        #self.__commands.append(self.clone_step(commit='34a70fa16497fd81ac2940f9e4a7c96bbfb31e86',
        #                                       repository='git://github.com/google/brax.git',
        #                                       path=self.__wd, directory='brax'))

        # Configure and Install
        #self.__commands.append(f"cd {self.__wd}/brax/")
        #self.__commands.append("pip3 install -e .")
        #self.__commands.append(f"cd {self.__wd}")
        
        # Cleanup directory
        #self.__commands.append( self.cleanup_step([ posixpath.join(self.__wd, 'brax') ] ))


