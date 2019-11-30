""" magnum building block"""

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
from hpccm.primitives.environment import environment



class magnum(bb_base, hpccm.templates.git, hpccm.templates.rm):

    def __init__(self, **kwargs):
        """Initialize building block"""

        super(magnum, self).__init__(**kwargs)

        self.__ospackages = kwargs.get('ospackages', ['ca-certificates',
                                                      'git',
                                                      'cmake',
                                                      'pkg-config',
                                                      'libglfw3-dev',
                                                      'libglfw3',
                                                      'libopenal-dev',
                                                      'libassimp-dev',
                                                      'libjpeg-dev',
	                                              'libpng-dev'])
        
        self.__workspace = kwargs.get('workspace', '/workspace')
        self.__dart = kwargs.get('dart', True)

        
        self.__commands = [] # Filled in by __setup()
        self.__tests = [] # Filled in by __setup()
        self.__wd = '/git' # working directory

        # Construct the series of steps to execute
        self.__setup()

        # Fill in container instructions
        self.__instructions()

    def __instructions(self):
        """Fill in container instructions"""

        self += comment('====INSTALLING MAGNUM=====')
        self += packages(ospackages=self.__ospackages)
        self += shell(commands=self.__commands)
        self += comment('====DONE MAGNUM=====')

    def __setup(self):
        """Construct the series of shell commands, i.e., fill in
           self.__commands"""


        ## CORRADE
        # Clone source
        self.__commands.append(self.clone_step(branch='master',
            repository='https://github.com/mosra/corrade.git',
            path=self.__wd, directory='corrade'))

        # Configure and Install
        self.__commands.append('mkdir ' + self.__wd+'/corrade/build')
        self.__commands.append('cd ' + self.__wd+'/corrade/build')

        self.__commands.append('cmake -DCMAKE_INSTALL_PREFIX:PATH='+self.__workspace+' ..')
        self.__commands.append('make -j')
        self.__commands.append('make install')

        ## MAGNUM
        # Clone source
        self.__commands.append(self.clone_step(branch='master',
            repository='https://github.com/mosra/magnum.git',
            path=self.__wd, directory='magnum'))

        # Configure and Install
        self.__commands.append('mkdir ' + self.__wd+'/magnum/build')
        self.__commands.append('cd ' + self.__wd+'/magnum/build')

        self.__commands.append('cmake -DCMAKE_INSTALL_PREFIX:PATH='+self.__workspace+' -DWITH_AUDIO=ON -DWITH_DEBUGTOOLS=ON -DWITH_GL=ON -DWITH_MESHTOOLS=ON -DWITH_PRIMITIVES=ON -DWITH_SCENEGRAPH=ON -DWITH_SHADERS=ON -DWITH_TEXT=ON -DWITH_TEXTURETOOLS=ON -DWITH_TRADE=ON -DWITH_GLFWAPPLICATION=ON -DWITH_WINDOWLESSGLXAPPLICATION=ON -DWITH_OPENGLTESTER=ON -DWITH_ANYAUDIOIMPORTER=ON -DWITH_ANYIMAGECONVERTER=ON -DWITH_ANYIMAGEIMPORTER=ON -DWITH_ANYSCENEIMPORTER=ON -DWITH_MAGNUMFONT=ON -DWITH_OBJIMPORTER=ON -DWITH_TGAIMPORTER=ON -DWITH_WAVAUDIOIMPORTER=ON .. ')
        self.__commands.append('make -j')
        self.__commands.append('make install')

        


        ## Magnum Plugins
        # Clone source
        self.__commands.append(self.clone_step(branch='master',
            repository='https://github.com/mosra/magnum-plugins.git',
            path=self.__wd, directory='magnum-plugins'))
        # Configure and Install
        self.__commands.append('mkdir ' + self.__wd+'/magnum-plugins/build')
        self.__commands.append('cd ' + self.__wd+'/magnum-plugins/build')
        
        self.__commands.append('cmake -DCMAKE_INSTALL_PREFIX:PATH='+self.__workspace+' -DWITH_ASSIMPIMPORTER=ON -DWITH_DDSIMPORTER=ON -DWITH_JPEGIMPORTER=ON -DWITH_OPENGEXIMPORTER=ON -DWITH_PNGIMPORTER=ON -DWITH_TINYGLTFIMPORTER=ON .. ')
        self.__commands.append('make -j')
        self.__commands.append('make install')

        if self.__dart:
            ## Magnum DART Integration (DART needs to be installed)
            # Clone source
            self.__commands.append(self.clone_step(branch='master',
                                                   repository='https://github.com/mosra/magnum-integration.git',
                                                   path=self.__wd, directory='magnum-integration'))
            # Configure and Install
            self.__commands.append('mkdir ' + self.__wd+'/magnum-integration/build')
            self.__commands.append('cd ' + self.__wd+'/magnum-integration/build')
            
            self.__commands.append('cmake -DCMAKE_INSTALL_PREFIX:PATH='+self.__workspace+'  -DWITH_DART=ON .. ')
            self.__commands.append('make -j')
            self.__commands.append('make install')


        # Cleanup directory
        self.__commands.append(self.cleanup_step(
                   [posixpath.join(self.__wd, 'corrade'),
                    posixpath.join(self.__wd, 'magnum'),
                    posixpath.join(self.__wd, 'magnum-plugins'),
                    posixpath.join(self.__wd, 'magnum-integration')]))

        
        
