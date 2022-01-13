import sys, getopt
from netmiko import ConnectHandler
import concurrent.futures as tr
import time
import csv
from pathlib import Path
import getpass
from os.path import exists
import re

##############################################################

#This script is to backup network devices (Routers/Switches/Firewalls/Load Balances).
#It required a configuration file (.txt) and hosts inventory (.csv) to work as explained in github.

###############################################################


log_time = str(time.strftime('%m-%d-%Y|%H:%M'))  # get the date and time for each log
dirct = str(time.strftime('%m-%d-%Y'))  # get the date of the backup
failed_ip = list()  # collect failed IPs
connection_times = {}
devices_count = {}
username = ""
password = ""


# defend color for terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# read devices form csv file
def read_devices(devicefile):
    global num_thread
    with open(devicefile, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for device in csv_reader:
            yield device


# get number of threads
def get_num_threads(devicefile):
    with open(devicefile, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        return len(list(csv_reader))


# get script argument
def check_argv():
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hi:", ["InventoryPath="])
    except getopt.GetoptError:
        print(
            f'{bcolors.FAIL}Error: Wrong syntax. Try <python GetNetBackup.py -h> for more information on usage{bcolors.ENDC}')
        sys.exit(2)

    if 2 >= len(argv) > 0 and not len(opts) == 0 and not args == 0:
        for opt, arg in opts:

            if opt == '-h' and len(argv) == 1:
                print(f'''{bcolors.WARNING}
                Usage: python GetNetBackup.py [ OPTION ] [ ARGUMENT ]
                -h,  help       
                -i,  --InventoryPath  The path to the inventory CSV file{bcolors.ENDC}''')
                sys.exit()

            elif opt in ("-i", "--InventoryPath "):
                inventory = arg
                file_exists = exists(inventory)
                if not file_exists and '.csv' not in inventory:
                    print('''
                           Invalid input.
                           Common causes of this problem are:
                           1. Missing Argument
                           2. Wrong file type
                           3. File does not exist
                           Or try python GetNetBackup.py -h for usage 
                                   ''')
                    sys.exit()
                else:
                    return inventory

            else:
                print(
                    f'{bcolors.FAIL}Error: Wrong syntax. Try <python GetNetBackup.py -h> for more information on usage{bcolors.ENDC}')
                sys.exit(2)
    else:
        print(
            f'{bcolors.FAIL}Error: Wrong syntax. Try <python GetNetBackup.py -h> for more information on usage{bcolors.ENDC}')
        sys.exit(2)

# get back configuration
def get_backup(device_data):
    global connection_times
    global devices_count
    cmd = device_data['backup']
    connect_device = {
        'device_type': device_data['dtype'],
        'ip': device_data['ip'],
        'username': username,
        'password': password,
    }
    # start connection
    while True:
        try:
            # count the number of the connection (for re-try option)
            if device_data["ip"] not in connection_times:
                connection_times[device_data["ip"]] = 0
            else:
                connection_times[device_data["ip"]] = connection_times[device_data["ip"]] + 1

            net_connect = ConnectHandler(**connect_device)

            hostname = (net_connect.find_prompt()[:-1])  # get the hostname of the switch

            # to delete the username before the name of the device, and just for juniper
            if device_data["vendor"] == 'juniper':
                hostname = hostname.split('@')[1]

            # to avoid the complexity of F5 hostname
            if device_data["vendor"] == 'F5':
                hostname = str(f'{device_data["vendor"]}_{device_data["ip"]}')

            print(f'{bcolors.OKBLUE}# connected to {device_data["ip"]}{bcolors.ENDC}')

            output = net_connect.send_command(cmd)  # send the command to the switch

            try:
                # check if the directory exist if not create one
                backupConf = open('GetNetBackup.conf', 'r')
                backupPath = re.findall('{(.+?)}', backupConf.read())
                # check if the path has slash at the end
                if not backupPath[0].endswith('/'):
                    backupPath[0] = backupPath[0] + '/'
                Path(backupPath[0] + dirct + '/' + device_data["vendor"]).mkdir(parents=True, exist_ok=True)

                # create a configuration file such as files/weekly_backups/10-11-2020/juniper/DH-DR-FW-SRX.txt
                with open(backupPath[0] + str(dirct) + '/' + device_data[
                    "vendor"] + '/' + hostname + '.txt',
                          'w') as write_file:
                    write_file.write(output)
                    write_file.close()
                    print(f'{bcolors.OKGREEN}## configuration saved for {device_data["ip"]}{bcolors.ENDC}')

                # count the number of passed devices
                if device_data["vendor"] in devices_count:
                    devices_count[device_data["vendor"]] = devices_count[device_data["vendor"]] + 1
                else:
                    devices_count[device_data["vendor"]] = 1

                net_connect.disconnect()  # close connection
                break

            except:
                if connection_times[device_data["ip"]] < 2:
                    continue  # retry the connection again
                else:
                    print(
                        f'{bcolors.FAIL}Error: Issues accure saving configuration file for {device_data["ip"]}{bcolors.ENDC}')
                    failed_ip.append([device_data["ip"],
                                      f'{bcolors.FAIL}Error Type:\nError: Issues accure saving configuration file for {device_data["ip"] }{bcolors.ENDC}'])
                    net_connect.disconnect()  # close connection
                    break  # break out of the loop if retry is completed

        except:
            if connection_times[device_data["ip"]] < 2:
                continue  # retry the connection again
            else:
                print(f'{bcolors.FAIL}Error: Connection to {device_data["ip"]} failed{bcolors.ENDC}')
                failed_ip.append([device_data["ip"], f'Error Type: Connection to {device_data["ip"]} failed'])
                break  # break out of the loop if retry is completed


def main():
    global username
    global password

    inventory = check_argv()  # check the argument
    # get username and password
    check = True
    print('Please Enter Username and Password')
    while (check):
        username = input("Username:")
        password = getpass.getpass("Password for " + username + ":")
        if len(username) and len(password) == 0:
            check = True
        # to check space
        elif (" " in password):
            check = True
        else:
            check = False

    # start time
    start_time = (time.time())
    # Devices inventory
    device_data = read_devices(inventory)  # collect the switches IPs from the inventory

    num_thread = get_num_threads(inventory)  # get the number
    # write failed IP to a file (multi-threads)
    with tr.ThreadPoolExecutor(max_workers=num_thread) as ex:
        ex.map(get_backup, device_data)

    ##### display the result of the backup
    if any(devices_count.values()):

        print(f'\n{bcolors.OKGREEN}=========================={bcolors.ENDC}')
        print(f'{bcolors.OKGREEN}Successful backup:{bcolors.ENDC}')
        print(f'{bcolors.OKGREEN}=========================={bcolors.ENDC}')
        for device, count in devices_count.items():
            print(f'{bcolors.OKGREEN}{device}: {count}{bcolors.ENDC}')
            print(f'{bcolors.OKGREEN}-------------------------------------------{bcolors.ENDC}')

    # if there are failed backup
    if len(failed_ip) > 0:
        print(f'{bcolors.FAIL}Failed Backup:{bcolors.ENDC}')
        print(f'{bcolors.FAIL}=========================={bcolors.ENDC}')
        for fail in failed_ip:
            print(f'{bcolors.FAIL}{fail[0]}: {fail[1]}{bcolors.ENDC}')
            print(f'{bcolors.FAIL}-------------------------------------------{bcolors.ENDC}')

    print(f'{bcolors.WARNING}###  Total time: {round(time.time() - start_time)} Seconds{bcolors.ENDC}')


if __name__ == '__main__':
    main()
