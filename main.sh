#!/bin/bash

sudo apt update && apt install mysql-server libmysqlclient-dev libxml2-dev libmemcached-dev memcached php-pear php-dev redis-server -y
pip3 install -r requirements.txt
sudo python3 main.py