#!/bin/bash

sudo apt update && apt install libmysqlclient-dev libpython3.7-minimal libpcap-dev -y && pip3 install -r requirements.txt && sudo python3 main.py
echo "Done."