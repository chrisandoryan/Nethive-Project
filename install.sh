#!/bin/bash
sudo apt update && apt install libxml2-dev curl apt-transport-https ca-certificates curl software-properties-common snapd pkg-config python3-pip python3 python-dev python3-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev -y
# go get github.com/jbowtie/gokogiri
docker-compose -f thirdparties/docker-elk/docker-compose.yml build 
docker-compose -f thirdparties/kafka-docker/docker-compose.yml build
