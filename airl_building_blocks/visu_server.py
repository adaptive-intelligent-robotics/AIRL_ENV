""" visu_server building block"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import posixpath

import hpccm.config
import hpccm.templates.git
import hpccm.templates.rm
import hpccm.templates.wget


from hpccm.building_blocks.base import bb_base
from hpccm.primitives.comment import comment
from hpccm.primitives.workdir import workdir
from hpccm.primitives.shell import shell
from hpccm.primitives.copy import copy
from hpccm.primitives.environment import environment
from hpccm.building_blocks.packages import packages

class visu_server(bb_base, hpccm.templates.git, hpccm.templates.rm, hpccm.templates.wget):

    def __init__(self, **kwargs):
        """Initialize building block"""

        super(visu_server, self).__init__(**kwargs)

        self.__ospackages = kwargs.get('ospackages', ['ca-certificates',
                                                      'git',
                                                      'wget',
                                                      'python3',
                                                      'python3-setuptools',
                                                      'libglu1-mesa',
                                                      'libgl1-mesa-dri',
	                                              'libxtst6',
                                                      'libxv1',
	                                              'x11-xkb-utils',
	                                              'xauth',
	                                              'openbox',
	                                              'xterm',
                                                      'emacs',
                                                      'vim'])

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

        self += comment('INSTALLING HEXAPOD_COMMON')
        self += packages(ospackages=self.__ospackages)
        self += copy(src='resources/visu_server', dest='/tmp_visu/')
        self += environment(variables={'LD_LIBRARY_PATH':self.__workspace +'/lib:$LD_LIBRARY_PATH','PATH':self.__workspace+'/bin:$PATH'})
        self += shell(commands=self.__commands)
        self += shell(commands=self.__tests, _test=True)

    def __setup(self):
        """Construct the series of shell commands, i.e., fill in
           self.__commands"""
        # Download packets
        self.__commands.append(self.download_step(url='https://svwh.dl.sourceforge.net/project/turbovnc/2.2.3/turbovnc_2.2.3_amd64.deb',directory=self.__wd))
        self.__commands.append(self.download_step(url='https://svwh.dl.sourceforge.net/project/virtualgl/2.6.3/virtualgl_2.6.3_amd64.deb',directory=self.__wd))
        self.__commands.append(self.download_step(url='https://netix.dl.sourceforge.net/project/libjpeg-turbo/2.0.3/libjpeg-turbo-official_2.0.3_amd64.deb',directory=self.__wd))

        self.__commands.append('cd /git')
        self.__commands.append('dpkg -i *.deb')
        self.__commands.append(self.cleanup_step(
            [posixpath.join(self.__wd, 'turbovnc_2.2.3_amd64.deb'),
            posixpath.join(self.__wd, 'virtualgl_2.6.3_amd64.deb'),
            posixpath.join(self.__wd, 'libjpeg-turbo-official_2.0.3_amd64.deb')]))

        self.__commands.append("sed -i 's/$host:/unix:/g' /opt/TurboVNC/bin/vncserver")

        self.__commands.append('mv /tmp_visu/visu_server/etc/X11 /etc/X11')
        self.__commands.append('mv /tmp_visu/visu_server/etc/skel/.xinitrc /etc/skel/')
        self.__commands.append('mv /tmp_visu/visu_server/etc/xdg/openbox /etc/xdg/openbox')
        self.__commands.append('mv /tmp_visu/visu_server/etc/turbovncserver.conf /etc/turbovncserver.conf')
        self.__commands.append('mv /tmp_visu/visu_server/.vnc /opt/.vnc')
        self.__commands.append('chmod og-rw /opt/.vnc/passwd')
        self.__commands.append('mkdir -p '+self.__workspace+'/bin')
        self.__commands.append('mv /tmp_visu/visu_server/bin/visu_server.sh '+self.__workspace+'/bin')

        self.__commands.append('rm -r /tmp_visu/visu_server')
        
        # Clone source
        self.__commands.append(self.clone_step(branch='v0.9.0',
                                               repository='https://github.com/novnc/websockify.git',
                                               path=self.__wd, directory='/opt/websockify'))

        # Configure and Install
        self.__commands.append('cd /opt/websockify')
        self.__commands.append('python3 setup.py install')


        # Clone source
        self.__commands.append(self.clone_step(branch='master',
                                               repository='https://github.com/kanaka/noVNC.git',
                                               path=self.__wd, directory='/opt/noVNC'))

        # Configure and Install
        self.__commands.append('cd /opt/noVNC')
        self.__commands.append('ln -s vnc_lite.html index.html')


        # TEST
        #self.__tests.append('visu_server.sh test')
