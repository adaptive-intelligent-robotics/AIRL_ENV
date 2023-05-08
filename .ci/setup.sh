#!/bin/bash


sudo apt-get update && apt-get install -y wget git \
                                          build-essential \
                                          squashfs-tools \
                                          libtool \
                                          autotools-dev \
                                          libarchive-dev \
                                          automake \
                                          autoconf \
                                          uuid-dev \
                                          libssl-dev


sed -i -e 's/^Defaults\tsecure_path.*$//' /etc/sudoers

# Check Python

echo "Python Version:"
python --version
pip install sregistry[all]
pip install hpccm
sregistry version

echo "sregistry Version:"

# Install Singularity

cd /tmp && \
    git clone -b v3.4.0 https://github.com/sylabs/singularity.git
    cd singularity && \
    ./autogen.sh && \
    ./configure --prefix=/usr/local && \
    make && make install


