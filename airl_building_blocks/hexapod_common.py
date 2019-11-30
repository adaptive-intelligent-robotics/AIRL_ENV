""" Hexapod_common building block"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import posixpath

import hpccm.config
import hpccm.templates.git
import hpccm.templates.rm

from hpccm.building_blocks.base import bb_base
from hpccm.primitives.comment import comment
from hpccm.primitives.workdir import workdir
from hpccm.primitives.shell import shell
from hpccm.building_blocks.packages import packages

class hexapod_common(bb_base, hpccm.templates.git, hpccm.templates.rm):

    def __init__(self, **kwargs):
        """Initialize building block"""

        super(hexapod_common, self).__init__(**kwargs)

        self.__ospackages = kwargs.get('ospackages', ['ca-certificates', 'git'])
        self.__commands = [] # Filled in by __setup()
        self.__wd = '/git' # working directory

        # Construct the series of steps to execute
        self.__setup()

        # Fill in container instructions
        self.__instructions()

    def __instructions(self):
        """Fill in container instructions"""

        self += comment('INSTALLING HEXAPOD_COMMON')
        self += packages(ospackages=self.__ospackages)
        self += shell(commands=self.__commands)


    def __setup(self):
        """Construct the series of shell commands, i.e., fill in
           self.__commands"""

        # Clone source
        self.__commands.append(self.clone_step(branch='master',
            repository='https://github.com/resibots/hexapod_common.git',
            path=self.__wd, directory='hexapod_common'))

        # Configure and Install
        self.__commands.append('cd /git/hexapod_common/hexapod_controller')
        self.__commands.append('./waf configure --prefix /workspace')
        self.__commands.append('./waf install')

        # Cleanup directory
        self.__commands.append(self.cleanup_step(
            [posixpath.join(self.__wd, 'hexapod_common')]))
