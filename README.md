# GetNetBackup
## Description
##### `GetNetBackup` is a network automation tool that helps network administration and network engineers collect routers, switches, firewalls, and load balancers configurations and store them in a specific folder with a date titled. It is an easy-to-use tool and does not require a programming background.

## Supported Vendors Devices
##### below is the list of supported vendor devices by GetNetBackup based on the Netmiko library. 
  - Arista EOS
  - Cisco ASA
   -Cisco IOS/IOS-XE
  - Cisco IOS-XR
  - Cisco NX-OS
  - Cisco SG300
  - HP Comware7
  - HP ProCurve
  - Juniper Junos
  - F5 TMSH
  - Aruba

## Prerequisite
##### For GetNetBackup to function, th following system packages must be installed.
- Centos and RedHat
```
sudo yum groupinstall 'Development Tools' -y
```
```
sudo yum install libffi-devel  openssl-devel -y
```
- Ubuntu
```
apt-get install build-essential libssl-dev libffi-dev -y
```
## Installation
#### Install python3 and git
* Centos and RedHat
```
sudo yum install python3 -y
```
```
sudo yum install python3-pip
```
```
sudo yum install git
```
* ubuntu
```
apt-get install python3 -y
```
```
apt-get install python3-pip
```
```
apt-get install git
```

#### Install the GetNetBackup
```
git clone https://github.com/abdulrahmanAbduatif/GetBackup.git
```
```
cd GetNetBackup
```
###### You might need to run it with sudo (root)
```
pip3 install -r requirements.txt
````

## Configuration
- Setting the backup path configuration
The configuration

