#!/bin/bash

sudo apt-get install git curl apt-transport-https ca-certificates curl software-properties-common snapd libmysqlclient-dev -y

# --- Docker
sudo snap install docker

# --- Filebeat
curl https://packages.elasticsearch.org/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://packages.elastic.co/beats/apt stable main" | sudo tee -a /etc/apt/sources.list.d/beats.list
echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list

# --- Fetch dependencies
sudo apt-get update && sudo apt-get install filebeat auditbeat heartbeat -y

# --- Docker-elk Repository
if [[ -z "${DOCKER_ELK_REPO_PATH}" ]]; then
  echo "DOCKER_ELK_REPO_PATH env is not set."
else
    rm -rfI ${DOCKER_ELK_REPO_PATH}
    git clone https://github.com/deviantony/docker-elk.git ${DOCKER_ELK_REPO_PATH}
fi