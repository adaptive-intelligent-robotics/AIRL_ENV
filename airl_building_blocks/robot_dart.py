""" robot_dart building block"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import hpccm.config
import hpccm.templates.git

from hpccm.building_blocks.base import bb_base
from hpccm.building_blocks.pip import pip
from hpccm.primitives.comment import comment
from hpccm.primitives.workdir import workdir
from hpccm.primitives.shell import shell
from hpccm.building_blocks.packages import packages
from hpccm.primitives.environment import environment
from airl_building_blocks.dart import dart
from airl_building_blocks.magnum import magnum


class robot_dart(bb_base, hpccm.templates.git):

    def __init__(self, **kwargs):
        """Initialize building block"""

        super(robot_dart, self).__init__(**kwargs)

        self.__ospackages = kwargs.get('ospackages', ['ca-certificates',
                                                      'git',
                                                      'ffmpeg',
                                                      'libeigen3-dev',
                                                      'python3-dev',
                                                      'libboost-filesystem-dev',
                                                      'libboost-system-dev',
                                                      'libboost-regex-dev',
                                                      'libboost-test-dev'])
        self.__simd = kwargs.get('simd', True)
        self.__magnum = kwargs.get('magnum', True)
        self.__hexapod_common = kwargs.get('hexapod_common', True)
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

        self += comment('====INSTALLING ROBOT_DART=====')
        self += packages(ospackages=self.__ospackages)
        self += environment(variables={'LD_LIBRARY_PATH':self.__workspace +'/lib:$LD_LIBRARY_PATH',
                                       'PATH':self.__workspace+'/bin:$PATH',
                                       'LC_ALL': 'C'})

        self += dart(simd=self.__simd)

        if self.__magnum:
            self += magnum()
        
        
        self += shell(commands=self.__commands)
        self += shell(commands=self.__tests, _test=True)
        self += comment('====DONE ROBOT_DART=====')

    def __setup(self):
        """Construct the series of shell commands, i.e., fill in
           self.__commands"""

        # Clone source
        self.__commands.append(self.clone_step(commit='95d615b004c60c4d5352c3db2af138c2c63f570f',
            repository='https://github.com/resibots/robot_dart.git',
            path=self.__wd, directory='robot_dart'))
        self.__commands.append('cd ' + self.__wd + '/robot_dart')

        # Change wscript to be more fine grained in the instruction set.
        self.__commands.append("sed -i 's/-march=native/-mavx -msse -msse2 '/g ./wscript")
        
        # Configure and Install
        config = './waf configure --python  --prefix ' + self.__workspace + ' --dart '+self.__workspace + ' --shared'
        if self.__magnum:
            config += ' --magnum_install_dir  ' + self.__workspace + ' --magnum_integration_install_dir ' + self.__workspace + ' --magnum_plugins_install_dir ' + self.__workspace + ' --corrade_install_dir ' + self.__workspace
        #if self.__hexapod_common:
        #    config += ' --controller ' + self.__workspace 
        self.__commands.append(config)
        self.__commands.append('./waf')
        self.__commands.append('./waf install')
        self.__commands.append('./waf clean')
                
        self.__tests.append('export LD_LIBRARY_PATH='+self.__workspace+'/lib:$LD_LIBRARY_PATH')
        self.__tests.append('export PATH='+self.__workspace+'/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin')
        self.__tests.append('cd /git/robot_dart')
        self.__tests.append('./waf examples')
        self.__tests.append('./build/hexapod_plain')

