#!/bin/bash

sudo apt-get install git curl apt-transport-https ca-certificates curl software-properties-common snapd libmysqlclient-dev

# --- Docker
sudo snap install docker

# --- Filebeat
git clone https://github.com/deviantony/docker-elk.git $1
curl https://packages.elasticsearch.org/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://packages.elastic.co/beats/apt stable main" | sudo tee -a /etc/apt/sources.list.d/beats.list

# --- Fetch dependencies
sudo apt-get update && sudo apt-get install filebeat