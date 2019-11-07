mkdir -p beats-forwarder/etc && cd beats-forwarder
curl -OL https://github.com/logmatic/beats-forwarder/releases/download/v0.1-rc1/beats-forwarder
cd etc && curl -OL https://raw.githubusercontent.com/logmatic/beats-forwarder/dev/etc/config.yml
cd ..
chmod +x beats-forwarder