#!/usr/bin/env bash

alias mdrmi='docker rmi $(docker images -f "dangling=true" -q)'
alias mdrm='docker rm $(docker ps -aq)'
alias mdrmf='docker rm -f $(docker ps -aq)'
alias mdocker='docker run -it --rm'
alias mdpa='docker ps -a'
alias mdi='docker images'
alias mdrmv='docker volume rm $(docker volume ls -q)'
alias mdev='docker run --name=mdev --rm -it maguowei/base'
