FROM gcr.io/gem5-test/ubuntu-20.04_all-dependencies:v22-1

ARG USER=docker
ARG GROUP=docker
ARG PASSWORD=docker
ARG HOME=/home/${USER}

ARG UID=1000097
ARG GID=1000001

ARG DEBIAN_FRONTEND=noninteractive

# LABEL maintainer="hychiu"

RUN groupadd -g ${GID} ${GROUP} && useradd -m ${USER} --uid=${UID} --gid=${GID} && echo "${USER}:${PASSWORD}" | chpasswd

# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC
RUN apt-get update && apt-get install
RUN apt-get install -y sudo && adduser ${USER} sudo
RUN apt-get install -y vim wget unzip gdb cmake
RUN apt-get install -y python3 python3-dev python3-pip
RUN apt-get install -y locales
RUN apt-get clean

RUN echo "${USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN python3 -m pip install -U pip
RUN python3 -m pip install numpy onnx onnxruntime

RUN locale-gen en_US.UTF-8

USER ${UID}:${GID}
WORKDIR ${HOME}/workspace

RUN cd /home/docker && echo "export LC_ALL=en_US.UTF-8" >> .bashrc
RUN cd /home/docker && echo "export TERM=xterm-256color" >> .bashrc
RUN cd /home/docker && echo "export PATH=$PATH:/home/docker/.local/bin" >> .bashrc
