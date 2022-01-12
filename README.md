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
