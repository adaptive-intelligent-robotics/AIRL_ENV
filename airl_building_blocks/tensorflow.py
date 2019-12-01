""" tensorflow building block"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import hpccm.config
import hpccm.templates.git

from hpccm.building_blocks.base import bb_base
from hpccm.primitives.comment import comment
from hpccm.primitives.workdir import workdir
from hpccm.primitives.shell import shell
from hpccm.building_blocks.packages import packages
from hpccm.primitives.environment import environment
from airl_building_blocks.dart import dart
from airl_building_blocks.magnum import magnum


class tensorflow(bb_base, hpccm.templates.git):

    def __init__(self, **kwargs):
        """Initialize building block"""

        super(tensorflow, self).__init__(**kwargs)

        self.__ospackages = kwargs.get('ospackages', ['ca-certificates',
                                                      'git',
                                                      'curl',
                                                      'libcurl3-dev',
                                                      'libfreetype6-dev',
                                                      'libhdf5-serial-dev',
                                                      'libzmq3-dev',
	                                              'libtool',
                                                      'python-dev',
                                                      'rsync',
                                                      'software-properties-common',
                                                      'unzip',
                                                      'zip',
                                                      'zlib1g-dev'])

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

        self += comment('====INSTALLING ROBOT_DART=====')
        self += packages(ospackages=self.__ospackages)
        self += environment(variables={'LD_LIBRARY_PATH':self.__workspace +'/lib:$LD_LIBRARY_PATH','PATH':self.__workspace+'/bin:$PATH'})
        self += dart(simd=self.__simd)
        if self.__magnum:
            self += magnum()
        self += shell(commands=self.__commands)
        self += shell(commands=self.__tests, _test=True)
        self += comment('====DONE ROBOT_DART=====')

    def __fix_cuda(self):
        self.__commands.append("find /usr/local/cuda-10.0/lib64/ -type f -name 'lib*_static.a' -not -name 'libcudart_static.a' -delete")
        self.__commands.append("rm /usr/lib/x86_64-linux-gnu/libcudnn_static_v7.a")

    def __setup_bazel(self):
        # Running bazel inside a `docker build` command causes trouble, cf:
	#   https://github.com/bazelbuild/bazel/issues/134
	# The easiest solution is to set up a bazelrc file forcing --batch.
	self.__commands.append('echo "startup --batch" >>/etc/bazel.bazelrc')

	# Similarly, we need to workaround sandboxing issues:
	#   https://github.com/bazelbuild/bazel/issues/418
	self.__commands.append('echo "build --spawn_strategy=standalone --genrule_strategy=standalone">>/etc/bazel.bazelrc')
	
	# Install the most recent bazel release.
	self.__commands.append("export BAZEL_VERSION=0.24.1")
	self.__commands.append("mkdir /bazel && cd /bazel")
	self.__commands.append('curl -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36" -fSsL -O https://github.com/bazelbuild/bazel/releases/download/$BAZEL_VERSION/bazel-$BAZEL_VERSION-installer-linux-x86_64.sh')
	self.__commands.append('curl -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36" -fSsL -o /bazel/LICENSE.txt https://raw.githubusercontent.com/bazelbuild/bazel/master/LICENSE')
	self.__commands.append("chmod +x bazel-*.sh")
	self.__commands.append("./bazel-$BAZEL_VERSION-installer-linux-x86_64.sh")
	self.__commands.append("cd / && rm -f /bazel/bazel-$BAZEL_VERSION-installer-linux-x86_64.sh")

	self.__commands.append("curl -fSsL -O https://bootstrap.pypa.io/get-pip.py")
	self.__commands.append("python3 get-pip.py")
    	self.__commands.append("rm get-pip.py")
	self.__commands.append("pip3 --no-cache-dir install Pillow h5py ipykernel jupyter keras_applications keras_preprocessing matplotlib mock numpy scipy sklearn future pandas ")
        
	self.__commands.append("python3 -m ipykernel.kernelspec")

     
        
    def __setup(self):
        """Construct the series of shell commands, i.e., fill in
           self.__commands"""

        # Clone source
        self.__commands.append(self.clone_step(branch='master',
            repository='https://github.com/resibots/robot_dart.git',
            path=self.__wd, directory='robot_dart'))

        # Configure and Install
        self.__commands.append('cd ' + self.__wd + '/robot_dart')
        config = './waf configure --prefix ' + self.__workspace + ' --dart '+self.__workspace + ' --shared'
        if self.__magnum:
            config += ' --magnum_install_dir  ' + self.__workspace + ' --magnum_integration_install_dir ' + self.__workspace + ' --magnum_plugins_install_dir ' + self.__workspace + ' --corrade_install_dir ' + self.__workspace
        if self.__hexapod_common:
            config += ' --controller ' + self.__workspace 
        self.__commands.append(config)
        self.__commands.append('./waf')
        self.__commands.append('./waf install')
        self.__commands.append('./waf clean')

        
        self.__tests.append('export LD_LIBRARY_PATH='+self.__workspace+'/lib:$LD_LIBRARY_PATH')
        self.__tests.append('cd /git/robot_dart')
        self.__tests.append('./waf')
        self.__tests.append('./build/pendulum_plain')
        


