""" dart building block"""

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


class dart(bb_base, hpccm.templates.git, hpccm.templates.rm):

    def __init__(self, **kwargs):
        """Initialize building block"""

        super(dart, self).__init__(**kwargs)

        self.__ospackages = kwargs.get('ospackages', ['ca-certificates',
                                                      'git',
                                                      'cmake',
	                                              'pkg-config',
                                                      'libeigen3-dev',
                                                      'libassimp-dev',
                                                      'libccd-dev',
                                                      'libfcl-dev',
                                                      'libassimp-dev',
	                                              'libccd-dev',
	                                              'libfcl-dev',
	                                              'libxi-dev',
	                                              'libxmu-dev',
	                                              'freeglut3-dev',
	                                              'libbullet-dev',
	                                              'libode-dev',
	                                              'libtinyxml2-dev',
	                                              'liburdfdom-dev',
                                                      'libboost-regex-dev',
                                                      'libboost-system-dev'])
        self.__simd = kwargs.get('simd', True)
        self.__commands = [] # Filled in by __setup()
        self.__wd = '/git' # working directory

        # Construct the series of steps to execute
        self.__setup()

        # Fill in container instructions
        self.__instructions()

    def __instructions(self):
        """Fill in container instructions"""

        self += comment('====INSTALLING DART====')
        self += packages(ospackages=self.__ospackages)
        self += shell(commands=self.__commands)
        self += comment('====DONE DART====')

    def __setup(self):
        """Construct the series of shell commands, i.e., fill in
           self.__commands"""

        # Clone source
        self.__commands.append(self.clone_step(branch='release-6.9',
                                               repository='git://github.com/dartsim/dart.git',
                                               path=self.__wd, directory='dart'))

        # Configure and Install
        self.__commands.append('mkdir /git/dart/build')
        self.__commands.append('cd /git/dart/build')
        if self.__simd:
            self.__commands.append('cmake -DDART_ENABLE_SIMD=ON -DCMAKE_INSTALL_PREFIX:PATH=/workspace ..')
        else:
            self.__commands.append('cmake -DCMAKE_INSTALL_PREFIX:PATH=/workspace ..')
        self.__commands.append('make -j install')


        # Cleanup directory
        self.__commands.append( self.cleanup_step([ posixpath.join(self.__wd, 'dart') ] ))
