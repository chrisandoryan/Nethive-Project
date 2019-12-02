# Blackhead
Restructured and Collaborated SIEM and CVSS Infrastructure

# Setup

```
$ docker run -p 6379:6379 -it --rm redislabs/redistimeseries
$ python3 ./Blackhead/main.py
$ cd ./beats-forwarder && ./beats-forwarder -c etc/config.yml
$ cd ./Blackhead/processors/xss_auditor && ./xss_auditor
```

