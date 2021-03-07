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


class dart(bb_base, hpccm.templates.git, hpccm.templates.rm):

    def __init__(self, **kwargs):
        """Initialize building block"""

        super(dart, self).__init__(**kwargs)

        self.__ospackages = kwargs.get('ospackages', ['ca-certificates',
                                                      'build-essential',
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
                                                      'libopenscenegraph-dev',
	                                              'libbullet-dev',
	                                              'libode-dev',
	                                              'libtinyxml-dev',
	                                              'libtinyxml2-dev',
	                                              'liburdfdom-dev',
                                                      'libboost-regex-dev',
                                                      'libboost-all-dev',
                                                      'libboost-system-dev',
                                                      'pybind11-dev',
                                                      ])
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
        self += pip(packages=['numpy'], pip='pip3')
        self += shell(commands=self.__commands)
        
        self += comment('====DONE DART====')

    def __setup(self):
        """Construct the series of shell commands, i.e., fill in
           self.__commands"""

        # Clone source
        self.__commands.append(self.clone_step(commit='v6.9.4',
                                               repository='git://github.com/dartsim/dart.git',
                                               path=self.__wd, directory='dart'))

        # Configure and Install
        self.__commands.append(f"mkdir {self.__wd}/dart/build")
        self.__commands.append(f"cd {self.__wd}/dart/build")
        if self.__simd:
            self.__commands.append("sed -i 's/-march=native/-mavx -msse -msse2 -g -faligned-new '/g ../dart/CMakeLists.txt")
            self.__commands.append('cmake -DDART_ENABLE_SIMD=ON -DCMAKE_INSTALL_PREFIX:PATH=/workspace -DCMAKE_BUILD_TYPE=Release ..')
        else:
            self.__commands.append('cmake -DCMAKE_INSTALL_PREFIX:PATH=/workspace  -DCMAKE_BUILD_TYPE=Release  ..')
        self.__commands.append('make -j16 install')

        
        self.__install_dart_py()

        # Cleanup directory
        self.__commands.append( self.cleanup_step([ posixpath.join(self.__wd, 'dart') ] ))

    def __install_dart_py(self):
        self.__commands.append(f"cd {self.__wd}/dart")

        self.__commands.append(f"mkdir build_py") # we need a different folder
        self.__commands.append(f"cd build_py")
        self.__commands.append(f"cmake -DDART_BUILD_DARTPY=ON -DDART_ENABLE_SIMD=ON -DCMAKE_INSTALL_PREFIX:PATH=/workspace -DCMAKE_BUILD_TYPE=Release ..")
        self.__commands.append(f"make -j16")
        self.__commands.append(f"make install")
