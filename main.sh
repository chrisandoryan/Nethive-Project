#!/bin/bash

sudo apt update && apt install libmysqlclient-dev libxml2-dev libmemcached-dev memcached -y
pip3 install -r requirements.txt
sudo python3 main.py