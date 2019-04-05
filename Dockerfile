FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04 as install_sferes2
RUN apt-get update && apt-get install -y \
    libboost-dev \
    libboost-test-dev \
    libboost-filesystem-dev \
    libboost-program-options-dev \
    libboost-graph-parallel-dev \
    libboost-thread-dev \
    libboost-regex-dev \
    python \
    g++ \
    libeigen3-dev \
    python-simplejson \
    libboost-mpi-dev \
    openmpi-common \
    openmpi-bin \
    libgoogle-perftools-dev \
    git \
    wget \
    libtbb-dev \
    emacs \
&& rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH /usr/libx86_64-linux-gnu
RUN mkdir /git
WORKDIR /git
RUN git clone https://github.com/sferes2/sferes2.git && cd sferes2 && git checkout a35890af6b818bdafafe0bcaf36457bfd286ca12 && ./waf configure && ./waf build
RUN sed -i 's/-O3/-O3 -march=native -g -faligned-new '/g ./sferes2/wscript

FROM install_sferes2 as install_dart
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    libeigen3-dev \
    libassimp-dev \
    libccd-dev \
    libfcl-dev \
    libxi-dev \
    libxmu-dev \
    freeglut3-dev \
    libopenscenegraph-dev \
    libbullet-dev \
    libode-dev \
    libtinyxml2-dev \
    liburdfdom-dev \
&& rm -rf /var/lib/apt/lists/*

RUN mkdir /workspace
WORKDIR /git
RUN git clone git://github.com/dartsim/dart.git && cd /git/dart && git checkout release-7.0 && mkdir build && cd build
RUN cd ./dart/build && cmake -DDART_ENABLE_SIMD=ON -DCMAKE_INSTALL_PREFIX:PATH=/workspace .. && make -j6 install
# RUN rm -rf ./dart
ENV LD_LIBRARY_PATH /workspace/lib:/usr/libx86_64-linux-gnu


FROM install_dart as install_robot_dart
WORKDIR /git
RUN git clone https://github.com/resibots/robot_dart.git && cd robot_dart && git checkout multi_robot && ./waf configure --prefix /workspace --dart /workspace && ./waf && ./waf install
RUN git clone https://github.com/resibots/hexapod_common.git && cd hexapod_common/hexapod_controller && ./waf configure && ./waf install

