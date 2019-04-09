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
RUN git clone https://github.com/sferes2/sferes2.git && \
    cd sferes2 && \
    git checkout a35890af6b818bdafafe0bcaf36457bfd286ca12 && \
    ./waf configure && \
    ./waf build
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
RUN git clone git://github.com/dartsim/dart.git && \ 
    cd /git/dart && \
    git checkout release-7.0 && \
    mkdir build
RUN cd ./dart/build && \
    cmake -DDART_ENABLE_SIMD=ON -DCMAKE_INSTALL_PREFIX:PATH=/workspace .. && \
    make -j6 install
RUN rm -rf ./dart
ENV LD_LIBRARY_PATH /workspace/lib:/usr/libx86_64-linux-gnu


FROM install_dart as install_robot_dart
WORKDIR /git
RUN git clone https://github.com/resibots/robot_dart.git && \
    cd robot_dart && git checkout multi_robot && \
    ./waf configure --prefix /workspace --dart /workspace && \
    ./waf && \
    ./waf install
RUN git clone https://github.com/resibots/hexapod_common.git && \
    cd hexapod_common/hexapod_controller && \
    ./waf configure && \
    ./waf install

FROM install_robot_dart as install_visu_server
RUN apt-get update &&  DEBIAN_FRONTEND=noninteractive apt-get install -y \
  git \
  libgl1-mesa-dri \
  net-tools \
  openbox \
  sudo \
  tint2 \
  x11-xserver-utils \
  x11vnc \
  xinit \
  xserver-xorg-video-dummy \
  xserver-xorg-input-void \
  websockify \
  wget && \
  rm -f /usr/share/applications/x11vnc.desktop && \
  rm -rf /var/lib/apt/lists/*

COPY etc/skel/.xinitrc /etc/skel/.xinitrc
RUN useradd -m -s /bin/bash user
USER user
RUN cp /etc/skel/.xinitrc /home/user/
USER root
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/user

RUN git clone https://github.com/kanaka/noVNC.git /opt/noVNC && \
  cd /opt/noVNC && \ 
#  git checkout 6a90803feb124791960e3962e328aa3cfb729aeb && \
  ln -s vnc_lite.html index.html
# noVNC (http server) is on 6080, and the VNC server is on 5900
EXPOSE 6080 5900

COPY ./etc /etc
COPY ./usr /usr
ENV DISPLAY :0


CMD ["bash"]