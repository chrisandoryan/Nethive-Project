# User Guide

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
  - [Pre-requisites](#pre-requisites)
    - [Supported Platforms](#supported-platforms)
    - [Hardware](#hardware)
    - [Software](#software)
    - [Installing pre-requisites](#installing-pre-requisites)
  - [Procedure for installing](#procedure-for-installing)
    * [GitHub](#github)
  - [After installation](#after-installation)

## Introduction

**The Nethive Project** provides a Security Information and Event Management (SIEM) insfrastructure empowered by **CVSS** measurements. 

**Nethive Engine** monitors every request coming through HTTP protocol to detect and identify any attempt of SQL Injection attacks. It also anonymously monitors every SQL query response to provide a wide range of XSS protection for your server, with both Stored and Reflected XSS attacks fully covered.

**Nethive Auditing** watch everything that happens inside your valuable system, with your permission of course. This would detects any strange and suspicious activity inside the system, whether it is a post-exploitation attempt of an attacks, or simply someone you trust is making mistake inside your system.

**Nethive Dashboard** provides you with resourceful, sleek user inferface that gives you the advantage of knowing everything. From resource consumption to the recent read-write action, it gives you full detail of what's happening, in near real-time.

**Nethive CVSS** analyze the unfortunately already happening attacks and measure its vulnerability metrics, making sure you are ready to put your reports done in no time.


## Installation

### Pre-requisites

#### Supported Platforms
Nethive Project runs on Linux operating systems. It is compatible with Python 3.

#### Hardware
-  Linux OS / Raspberry Pi - have `sudo` access on the terminal/console
-  Mouse / Wireless Mouse / Touchpad congenital laptop

#### Software
-  Python 2.x or 3.x
-  Filebeat
-  Auditbeat
-  Packetbeat
-  Docker
-  Docker-Compose
-  Scapy

#### Installing pre-requisites
Python:
https://www.python.org/

Filebeat:

    $ wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
    $ sudo apt-get install apt-transport-https
    $ echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main"  | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
    $ sudo apt-get update && sudo apt-get install filebeat

Alternatively, you can follow the instructions provided on the official website: https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation.html

Auditbeat:
See [Filebeat](#filebeat)

Packetbeat:
See [Filebeat](#filebeat)

Docker:
https://www.docker.com/

Installation example for **Ubuntu 18.04**:
```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
$ sudo apt update && sudo apt install docker-ce
```
Docker-Compose:
https://docs.docker.com/compose/install/

```
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
```

#### Installation from Github

Installing from GitHub involves the following steps:

1.  Clone the repository:  
`$ git clone https://github.com/chrisandoryan/Nethive-Project.git`

2.  Navigate into the project directory: 
`$ cd Nethive-Project/`

3.  Install library dependencies:
`$ sudo bash install.sh`
    
3.  Install Python dependencies:
`$ sudo python3 -m pip install -r requirements.txt`
    
4.  Install Nethive package: 
`$ sudo python3 setup.py install`
    
If done, proceed to [After installation](https://github.com/chrisandoryan)

### After installation
#### Configuring Nethive environment

##### Editing the configurations using a text-editor
Nethive configuration should be stored in a file named ``.env`` and located on the root directory of the project.

1. Copy `.env.example` to `.env`
	```
	$ cd Nethive-Project/
	$ cp .env.example .env
	``` 
2. Edit using gedit: `$ gedit .env`
3. Save your changes and proceed to next section.

Default configuration:
```
# Nethive configuration
LISTEN_IFACE = "lo"

# MySQL Information
MYSQL_USER = "root"
MYSQL_PASS = ""
MYSQL_HOSTNAME = "127.0.0.1"
MYSQL_DB = ""

# Log File paths to be monitored
AUDIT_LOG_PATH = "/var/log/audit/audit.log"
MYSQL_SLOW_QUERY_LOG_PATH = "/var/log/mysql/slow-query.log"
PARSED_SLOW_QUERY_LOG_PATH = "/var/log/mysql/slog.log"
SQL_RESPONSE_LOG_PATH = "/var/log/mysql/responses.log"
HTTP_LOG_PATH = "/var/log/http/inbound.log"
CENTRALIZED_BASH_HISTORY_PATH = "/var/log/bash/history.log"

# Auditbeat configuration
AUDITBEAT_PATH = "/etc/auditbeat"
AUDITBEAT_CONFIG_PATH = "${AUDITBEAT_PATH}/auditbeat.yml"
AUDITBEAT_RULES_PATH = "${AUDITBEAT_PATH}/audit.rules.d/auditbeat.rules"

# Filebeat configuration
FILEBEAT_PATH = "/etc/filebeat"
FILEBEAT_CONFIG_PATH = "${FILEBEAT_PATH}/filebeat.yml"

# Packetbeat configuration
PACKETBEAT_PATH = "/etc/packetbeat"
PACKETBEAT_CONFIG_PATH = "${PACKETBEAT_PATH}/packetbeat.yml"

# Connection
LOGSTASH_HOST = "127.0.0.1"
LOGSTASH_PORT = 5000
AUDIT_CONTROL_HOST = "127.0.0.1"
AUDIT_CONTROL_PORT = "5129"
XSS_WATCHMAN_SOCKET = "/tmp/xss_auditor.sock"

# Kafka configuration
KAFKA_TOPIC = "NETHIVE"
KAFKA_BOOTSTRAP_SERVER = ["127.0.0.1:9092"]
```

##### Editing the configurations using interactive menu
[Coming soon!]

#### Running Nethive after configuration change
**Nethive** depends on some third party binaries, such as: Filebeat, Auditbeat, etc., and requires special configuration for some services, such as MySQL server, etc. When running for the first time, you need to make sure that those binaries and services are configured to work with **Nethive**.

> Important! **Nethive** needs a sudo permission to work.

 1. Start **Nethive** with superuser permission:  `$ sudo python3 main.py`
2. On the menu prompt, choose: 
**[2] Refresh Configuration** 
to apply your modified  `.env` configuration into the **Nethive** itself and to distribute Nethive-ready configuration for the third party dependencies (beats, etc.).

[Command preview GIF]

### Usage

### Introduction
Nethive-cvss is a low-latency, CVSS Summarizer that allows for quick estimation of risk from an event that is classified as a threat by the SIEM engine. The output of this summarizer is shaped in the following format


	{
		severity: < The severity of the vulnerability based on CVSS:3.0 severity range>,
		score : < The actual risk score >,
		vector: < The vector string representation of the vulnerability's risk >
	
	}

Nethive-CVSS requires a Kafka server to run. YOu can get a quick instance from here : 

### Required Env Variables

You would need to configure a MYSQL server, a table called `paths` must be inserted in your specified database with the following columns 
	
	  `superuser` tinyint(1) NOT NULL DEFAULT '0',
	  `authentication` tinyint(1) NOT NULL DEFAULT '0',
	  `paths` varchar(255) DEFAULT NULL,
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  PRIMARY KEY (`id`)
	

The Nethive-CVSS microservice requires you to specify several environment variables in order to work. The following is the list of envionment variables


	PRODUCER  		the topic name, which would connect
	BOOTSTRAP_SERVER 	the location of your Kafka server
	INTERFACE		IP/CIDR combination of the machine you wish to check
	ESLOC			Location of Elasticsearch
	STOREINDEX		The Elasticsearch index where you'd store new summarizing outputs
	MYSQL			The dsn to connect to a mysql server
				Format : [username[:password]@][protocol[(address)]]/dbname[?
				param1=value1&...&paramN=valueN]
				Example : test_user:test@/test
	

Where 

        - test_user is the user is the user of the database
        - test (before the @) is the password
        - you can simply just write @ to specify that the database is located in localhost
        - and the final *test* is the database name.
 

And the rest, is taken care for y

#### Nethive-CVSS
This microservice is required so that every detected attacks are measured automatically according to CVSS3.0 vulnerability measurement. A **Nethive Engine** will automatically send every detected attacks data into this docker container and the measurement result will be stored back into Elasticsearch to a specified index.

To run nethive-cvss docker:
```
$ git clone https://github.com/Falanteris/docker-nethive-cvss/
$ cd docker-nethive-cvss/
$ docker build -t nethive-cvss .
$ ./cvss
```

#### Nethive Engines
##### [1] Check Dependencies
[Coming soon!]
##### [2] Refresh Configuration
[Coming soon!]
##### [3] Just-Start-This-Thing
[Coming soon!]
##### [4] Exit
You know, just an ordinary exit menu. Meh.
#### Nethive Admin




