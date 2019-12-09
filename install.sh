#!/bin/bash

sudo apt update && apt install mysql-server libmysqlclient-dev libxml2-dev curl apt-transport-https ca-certificates curl software-properties-common snapd pkg-config -y

go get github.com/jbowtie/gokogiri
