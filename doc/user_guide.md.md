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
    * [Setting up a virtual environment(optional)](#setting-up-a-virtual-environment)
    * [GitHub](#github)
    * [Zip](#zip)
  - [After installation](#after-installation)
    *  [Configuring SecureTea](#configuring-securetea)
      -  [Editing the configurations using a text editor](#editing-the-configurations-using-a-text-editor)
          -  [Using Vim](#using-vim)
	     -  [Using gedit](#using-gedit)
      -  [Configuring using interactive setup mode](#configuring-using-interactive-setup-mode)
          - [Setup all the features](#setup-all-the-features)
	     - [Setup a particular feature](#setup-a-particular-feature)
      -  [Configuring using Web UI](#configuring-using-web-ui)
          - [Using local web server over HTTPS](/doc/en-US/web_https.md)
      -  [Configuring using CLI arguments](#configuring-using-cli-arguments)
    *  [Getting tokens](#getting-tokens)
        -  [Getting Twitter tokens](#getting-twitter-tokens)
	   -  [Getting Slack tokens](#getting-slack-tokens)
	   -  [Getting Telegram tokens](#getting-telegram-tokens)
        -  [Get Twilio SMS tokens](#getting-twilio-sms-tokens)
	   - [Get Gmail tokens](#getting-gmail-tokens)

## Introduction

**The Nethive Project** provides a Security Information and Event Management (SIEM) insfrastructure empowered by **CVSS** measurements. 

**Nethive Engine** monitors every request coming through HTTP protocol to detect and identify any attempt of SQL Injection attacks. It also anonymously monitors every SQL query response to provide a wide range of XSS protection for your server, with both Stored and Reflected XSS attacks fully covered.

**Nethive Auditing** watch everything that happens inside your valuable system, with your permission of course. This would detects any strange and suspicious activity inside the system, whether it is a post-exploitation attempt of an attacks, or simply someone you trust is making mistake inside your system.

**Nethive Dashboard** provides you with resourceful, sleek user inferface that gives you the advantage of knowing everything. From resource consumption to the recent read-write action, it gives you full detail of what's happening, in near real-time.

**Nethive CVSS** analyze the unfortunately already happening attacks and measure its vulnerability metrics, making sure you are ready to put your reports done in no time.


## Installation

### Pre-requisites

#### Supported Platforms
Nethive Project runs on Linux operating systems. It is compatible with both Python 2 and Python 3.

#### Hardware
-  Linux OS / Raspberry Pi - have `sudo` access on the terminal/console
-  Mouse / Wireless Mouse / Touchpad congenital laptop

#### Software
-  Python 2.x or 3.x
-  Filebeat
-  Auditbeat
-  Packetbeat
-  Docker
-  Scapy

#### Installing pre-requisites
Python:
https://www.python.org/

Filebeat:

    wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
    sudo apt-get install apt-transport-https
    echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main"  | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
    sudo apt-get update && sudo apt-get install filebeat

Alternatively, you can follow the instructions provided on the official website: https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation.html

Auditbeat:
See [Filebeat](#filebeat)

Packetbeat:
See [Filebeat](#filebeat)

Docker:
https://www.docker.com/


