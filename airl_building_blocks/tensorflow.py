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
from hpccm.building_blocks.pip import pip
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
                                                      'rsync',
                                                      'software-properties-common',
                                                      'unzip',
                                                      'autoconf',
    	                                              'automake',
                                                      'zip',
                                                      'zlib1g-dev'])

        self.__simd = kwargs.get('simd', True)
        self.__workspace = kwargs.get('workspace', '/workspace')
        self.__bazel_version = kwargs.get('bazel_version', '0.24.1')
        self.__tf_branch = kwargs.get('tf_branch', 'r2.0')
        self.__cuda_compute_capabilities = kwargs.get('cuda_compute_capabilities', '3.5,5.2,6.0,6.1,7.0,7.5')
        self.__cuda_version = kwargs.get('cuda_version', '10.0')
        self.__cudnn_version = kwargs.get('cudnn_version', '7')
        
        self.__commands = [] # Filled in by __setup()
        self.__tests = [] # Filled in by __setup()
        self.__wd = '/git' # working directory

        # Construct the series of steps to execute
        self.__setup()

        # Fill in container instructions
        self.__instructions()

    def __instructions(self):
        """Fill in container instructions"""

        self += comment('====INSTALLING TENSORFLOW=====')
        self += packages(ospackages=self.__ospackages)
        self += pip(packages=['Pillow',
                              'h5py',
                              'ipykernel',
                              'jupyter',
                              'keras_applications',
                              'keras_preprocessing',
                              'matplotlib',
                              'mock',
                              'numpy',
                              'scipy',
                              'sklearn',
                              'future',
                              'pandas'],
                    pip='pip3')
        # self += environment(variables={'LD_LIBRARY_PATH':self.__workspace +'/lib:$LD_LIBRARY_PATH','PATH':self.__workspace+'/bin:$PATH'})
        
        
        self += shell(commands=self.__commands)
        self += shell(commands=self.__tests, _test=True)
        self += comment('====DONE TENSORFLOW=====')

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
        self.__commands.append("export BAZEL_VERSION=" + self.__bazel_version)
        self.__commands.append("mkdir /bazel && cd /bazel")
        self.__commands.append('curl -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36" -fSsL -O https://github.com/bazelbuild/bazel/releases/download/$BAZEL_VERSION/bazel-$BAZEL_VERSION-installer-linux-x86_64.sh')
        self.__commands.append('curl -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36" -fSsL -o /bazel/LICENSE.txt https://raw.githubusercontent.com/bazelbuild/bazel/master/LICENSE')
        self.__commands.append("chmod +x bazel-*.sh")
        self.__commands.append("./bazel-$BAZEL_VERSION-installer-linux-x86_64.sh")
        self.__commands.append("cd / && rm -f /bazel/bazel-$BAZEL_VERSION-installer-linux-x86_64.sh")

    def __setup_tensorflow(self):
        # Download and build TensorFlow.
        # Clone source
        self.__commands.append(self.clone_step(branch=self.__tf_branch,
            repository='https://github.com/tensorflow/tensorflow.git',
            path=self.__wd, directory='tensorflow'))
	
	# Configure the build for our CUDA configuration.
        self.__commands.append("export CI_BUILD_PYTHON=python3")
        self.__commands.append("export LD_LIBRARY_PATH=/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH")
        self.__commands.append("export TF_NEED_CUDA=1")
        self.__commands.append("export TF_NEED_TENSORRT=0")
        self.__commands.append("export TF_CUDA_COMPUTE_CAPABILITIES="+self.__cuda_compute_capabilities)
        self.__commands.append("export TF_CUDA_VERSION="+self.__cuda_version)
        self.__commands.append("export TF_CUDNN_VERSION="+self.__cudnn_version)

        self.__commands.append("ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/stubs/libcuda.so.1")


        self.__commands.append("cd "+self.__wd+"/tensorflow")
        self.__commands.append('LD_LIBRARY_PATH=/usr/local/cuda/lib64/stubs:${LD_LIBRARY_PATH} \
    	tensorflow/tools/ci_build/builds/configured GPU \
    	bazel build -c opt --local_resources=20000,40,1.0 --copt=-mavx --config=cuda \
    	--cxxopt="-D_GLIBCXX_USE_CXX11_ABI=1" \
    	//tensorflow/tools/pip_package:build_pip_package //tensorflow:libtensorflow_cc.so //tensorflow:libtensorflow_framework.so')

        self.__commands.append("rm /usr/local/cuda/lib64/stubs/libcuda.so.1")
        self.__commands.append("bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/pip")
        self.__commands.append("pip3 --no-cache-dir install --upgrade /tmp/pip/tensorflow-*.whl ")
    
        self.__commands.append("mkdir -p                "+self.__workspace+"/include/google/tensorflow") 
        self.__commands.append("cp -r bazel-genfiles/*  "+self.__workspace+"/include/google/tensorflow/")
        self.__commands.append("cp -r tensorflow        "+self.__workspace+"/include/google/tensorflow/")
        self.__commands.append('find                    '+self.__workspace+'/include/google/tensorflow -type f  ! -name "*.h" -delete')
        self.__commands.append("cp -r third_party       "+self.__workspace+"/include/google/tensorflow/")
        self.__commands.append("cp bazel-bin/tensorflow/lib*.so "+self.__workspace+"/lib")

        self.__commands.append("rm -rf /root/.cache ")
        self.__commands.append("rm -rf /git/tensorflow") 
        self.__commands.append("rm -rf /tmp/pip")



    def __setup_protobuf(self):
        # Careful, the version of Protobuf should match the version used by bazel
        self.__commands.append(self.clone_step(branch="v3.7.0",
                                               repository='https://github.com/google/protobuf',
                                               path=self.__wd, directory='protobuf'))
        self.__commands.append("cd protobuf")
        self.__commands.append("git submodule update --init --recursive")
        self.__commands.append("./autogen.sh")
        self.__commands.append("./configure --prefix="+self.__workspace)
        self.__commands.append("make -j64 install")
        self.__commands.append("cd ..")
        self.__commands.append("rm -Rf protobuf")

    def __setup_abseil(self):
        self.__commands.append(self.clone_step(branch="20180600",
                                               repository='https://github.com/abseil/abseil-cpp.git',
                                               path=self.__wd, directory='abseil-cpp'))
        self.__commands.append("cd abseil-cpp")
        self.__commands.append("mkdir build && cd build")
        self.__commands.append("cmake -DCMAKE_INSTALL_PREFIX:PATH="+self.__workspace+" ..")
        self.__commands.append("make -j")
        self.__commands.append("cp -r ../absl "+self.__workspace+"/include/")
        self.__commands.append('find   '+self.__workspace+'/include/absl -type f  -name "*.cc" -delete ')
        self.__commands.append("cd && rm -rf /git/absl-cpp")


        
    def __setup(self):
        """Construct the series of shell commands, i.e., fill in
           self.__commands"""
        self.__fix_cuda()
        self.__setup_bazel()
        self.__commands.append("python3 -m ipykernel.kernelspec")        
        self.__setup_tensorflow()
        #self.__setup_protobuf()
        #self.__setup_abseil()
