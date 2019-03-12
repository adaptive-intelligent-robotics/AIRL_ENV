FROM ubuntu:18.04 as install_sferes2
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
RUN mkdir /git && cd /git && git clone https://github.com/sferes2/sferes2.git && cd sferes2 && git checkout a35890af6b818bdafafe0bcaf36457bfd286ca12 && ./waf configure && ./waf build
 
FROM install_sferes2 as install_dart
RUN apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    libeigen3-dev \
    libassimp-dev \
    libccd-dev \
    libfcl-dev \
    libopenscenegraph-dev \
    libbullet-dev \
    libode-dev \
    libtinyxml2-dev \
    liburdfdom-dev \
&& rm -rf /var/lib/apt/lists/*

RUN mkdir /workspace
RUN cd /git && git clone git://github.com/dartsim/dart.git && cd /git/dart && git checkout release-7.0 && mkdir build && cd build
RUN cd /git/dart/build && cmake -DCMAKE_INSTALL_PREFIX:PATH=/workspace .. && make -j12 install
ENV LD_LIBRARY_PATH /workspace/lib:/usr/libx86_64-linux-gnu