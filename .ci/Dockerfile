FROM ubuntu:22.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
    software-properties-common \
    git \
    gpg-agent \
    && add-apt-repository -y ppa:apptainer/ppa \
    && apt update \
    && apt install -y apptainer \
    && rm -rf /var/lib/apt/lists/*

	
