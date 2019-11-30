""" sferes building block"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import hpccm.config
import hpccm.templates.git

from hpccm.building_blocks.base import bb_base
from hpccm.primitives.comment import comment
from hpccm.primitives.workdir import workdir
from hpccm.primitives.shell import shell
from hpccm.primitives.copy import copy
from hpccm.primitives.environment import environment
from hpccm.building_blocks.packages import packages

class sferes(bb_base, hpccm.templates.git):

    def __init__(self, **kwargs):
        """Initialize building block"""

        super(sferes, self).__init__(**kwargs)

        self.__ospackages = kwargs.get('ospackages', ['ca-certificates',
                                                      'git',                                                      
                                                      'libeigen3-dev',
                                                      'libtbb-dev',
                                                      'libboost-serialization-dev',
                                                      'libboost-filesystem-dev',
                                                      'libboost-system-dev',
                                                      'libboost-test-dev',
                                                      'libboost-program-options-dev',
                                                      'libboost-graph-dev',
                                                      'libboost-mpi-dev',
                                                      'libboost-thread-dev',
                                                      'libboost-regex-dev'])
        self.__simd = kwargs.get('simd', True)
        self.__workspace = kwargs.get('workspace', '/workspace')

        self.__commands = [] # Filled in by __setup()
        self.__tests = [] # Filled in by __setup()
        self.__wd = '/git' # working directory

        # Construct the series of steps to execute
        self.__setup()

        # Fill in container instructions
        self.__instructions()

    def __instructions(self):
        """Fill in container instructions"""

        self += comment('====INSTALLING SFERES====')
        self += packages(ospackages=self.__ospackages)
        self += copy(src='resources/sferes/ssrc', dest=self.__workspace+'/include/ssrc')
        self += environment(variables={'LD_LIBRARY_PATH':self.__workspace +'/lib:$LD_LIBRARY_PATH','PATH':self.__workspace+'/bin:$PATH'})
        self += shell(commands=self.__commands)
        self += shell(commands=self.__tests, _test=True)
	self += comment('====DONE SFERES====')


    def __setup(self):
        """Construct the series of shell commands, i.e., fill in
           self.__commands"""

        # Clone source
        self.__commands.append(self.clone_step(branch='qd',
            repository='https://github.com/sferes2/sferes2.git',
            path=self.__wd, directory='sferes2'))
        
        # Configure and Install
        self.__commands.append('cd ' + self.__wd + '/sferes2')
        if self.__simd:
            self.__commands.append("sed -i 's/-O3/-O3 -march=native -g -faligned-new '/g ./wscript")

        self.__commands.append('./waf configure --kdtree /workspace/include')

        #tests
        self.__tests.append('export LD_LIBRARY_PATH='+self.__workspace+'/lib:$LD_LIBRARY_PATH')
        self.__tests.append('export PATH='+self.__workspace+'/bin:$PATH')
        self.__tests.append('cd /git/sferes2')
        self.__tests.append('./waf')
        self.__tests.append('build/examples/ex_qd')
