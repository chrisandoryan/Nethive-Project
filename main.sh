#!/bin/bash

sudo apt update && apt install libmysqlclient-dev -y
pip3 install -r requirements.txt
sudo python3 main.py