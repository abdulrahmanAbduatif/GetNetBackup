# GetNetBackup
## Description
##### `GetNetBackup` is a network automation tool that helps network administration and network engineers collect routers, switches, firewalls, and load balancers configurations and store them in a specific folder with a date titled. It is an easy-to-use tool and does not require a programming background.

## Supported Vendors Devices
##### Below is the list of supported vendor devices by GetNetBackup based on the Netmiko library. 
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
* Ubuntu
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
- Setup the backup path configuration
##### The path configuration is in the GetNetBackup.conf. you can specify the backup path with the curly brackets. the default is `files/backup/`.

<img width="672" alt="Screen Shot 2022-01-13 at 1 53 38 PM" src="https://user-images.githubusercontent.com/8627674/149322475-7cebb0c7-e622-4e1b-b44e-a144f48bf419.png">

- Setup and understand the inventory
##### The inventory is just a CSV file that you can create yourself following the example file `inventory-test.csv`  or use `inventory-test.csv`  after updating it based on your device's inventory.
##### This is how it looks in Microsoft excel/Numbers

<img width="510" alt="Screen Shot 2022-01-13 at 2 41 29 PM" src="https://user-images.githubusercontent.com/8627674/149324515-62c7886f-0320-497b-abc6-e88fe08e6193.png">

##### This is on terminal

<img width="704" alt="Screen Shot 2022-01-13 at 2 42 19 PM" src="https://user-images.githubusercontent.com/8627674/149324610-229b533e-bfd6-4d3c-9e87-4bb76a001ec7.png">

##### **IP:** is just the devices IP address that you use to connect to the cli.
##### **dtype:** is the device driver type such as cisco_ios for cisco, juniper_jonos for juniper, and hp_procurve for HP. you can find the rest of supported devices [HERE](https://ktbyers.github.io/netmiko/docs/netmiko/index.html)
##### **vendor:** This is to specify the vendor name so the tool can arrange them in the correct folder.
##### **backup:** This is important. Here where you add the command line to read the configuration form the specific vendor device. For example Cisco and HP `show running-config` and Juniper `show configuration | display set | no-more`.

## Run GetNetBackup
##### Run the GetNetBackup.py file
```linux
$ python3 GetNetBackup.py -h

                Usage: python GetNetBackup.py [ OPTION ] [ ARGUMENT ]
                -h,  help       
                -i,  --InventoryPath  The path to the inventory CSV file

```
##### Take a backup
```
python3 GetNetBackup.py -i inventory-test.csv 
```

##### The output of the tools

##### The backup folder

## Have fun :wink: and keep automating :space_invader:
