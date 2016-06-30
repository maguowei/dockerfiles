FROM ubuntu:16.04
MAINTAINER Guowei Ma <imaguowei@gmail.com>

LABEL name="base"
LABEL version="16.04"

#RUN sed -i "s/archive.ubuntu.com/mirrors.aliyun.com/g" /etc/apt/sources.list

RUN locale-gen zh_CN.UTF-8
RUN locale-gen en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LC_CTYPE zh_CN.UTF-8

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    apt-utils \
    build-essential \
    libmysqlclient-dev \
    mysql-client \
    git \
    wget \
    curl \
    vim \
    zsh \
    python3.5-dev \
    python3-pip

RUN ln -sf /usr/bin/python3.5 /usr/bin/python3
RUN pip3 install -U pip

RUN git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh \
      && cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc \
      && chsh -s /bin/zsh

CMD zsh
