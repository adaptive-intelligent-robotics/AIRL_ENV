FROM ubuntu:18.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 \
    python3-distutils \
    build-essential \
    libssl-dev \
    uuid-dev \
    libgpgme11-dev \
    squashfs-tools \
    libseccomp-dev \
    wget \
    pkg-config \
    ca-certificates \
    cryptsetup-bin \
    uidmap \
    curl \
    git &&\
    ln -s /usr/bin/python3 /usr/bin/python
	
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py

# fix "mesg: ttyname failed: Inappropriate ioctl for device" warning
RUN cp /etc/profile /root/.profile

#RUN sed -i -e 's/^Defaults\tsecure_path.*$//' /etc/sudoers

# Check Python

RUN echo "Python Version:" && \
    python --version && \
    pip3 install hpccm && \
    pip3 install sregistry[all] && \
    echo "sregistry Version:" && \
    sregistry version

# Install GO
RUN export VERSION=1.12 OS=linux ARCH=amd64 && \
    wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz && \
    tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz && \
    rm go$VERSION.$OS-$ARCH.tar.gz

ENV PATH=/usr/local/go/bin:$PATH

# Install Singularity

RUN cd /tmp && \
    git clone -b v3.4.0 https://www.github.com/sylabs/singularity.git &&\
    cd singularity && \
    ./mconfig && \
    make -C builddir && \
    make -C builddir install

RUN echo "root:100000:65536" >> /etc/subuid && \
    echo "root:100000:65536" >> /etc/subgid

ADD ./sregistry_file /sregistry_file

CMD ["/bin/bash", "-c"]

