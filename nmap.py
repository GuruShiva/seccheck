__author__ = 'guru-main-linux'


import subprocess
import re
import sys

def net_menu():
    print "Initializing Network Scan: "
    print "Choose Network:  "
    print " #1- LAN"
    print " #2- WLAN"
    print " #3- EXIT"


loop = True

while loop:
    net_menu()
    choice = int ( raw_input("Please Enter The Network# To Scan: "))

    if choice == 1 :
      IPNet = '192.168.0.1/24' #Put your LAN Network/Mask here
      print "Scanning LAN Network Now"

    elif choice == 2 :
      IPNet = '192.168.1.1/24' #Put your WLAN Network/Mask here
      print "Scanning WLAN Network Now"


    elif choice== 3:
        print "Exiting Network Scan"
        sys.exit()
    else:
        # Any integer inputs other than values 1-3 we print an error message
        choice = int(raw_input("Wrong option selection. Enter any key to try again.."))



    nmap =  subprocess.check_output(['sudo','nmap', '-O' ,'-sT', IPNet]) #nmap script options


    parseNmap=nmap.split('\n') #parsing nmap script output


    MACAdd = [] #list of MAC Address found in output
    IPHost = [] #list of IP Address found in output
    HostStatus = [] #list of found Host status
    ListDevInfo = [] #combine IPHost and HostStatus

    MACAllowedList = ['38:59:F9:3C:88:71','40:E2:30:AE:14:ED','C0:EE:FB:25:8D:A6','C0:EE:FB:5A:7C:49','C8:D7:19:D3:DF:DB']


    for line in parseNmap:
       if line.startswith("MAC Address"):
          MACAdd.append(line) #Append list of MAC Address found in output
        

       elif line.startswith("Nmap scan report"):
          IPHost.append(line) #lAppend ist of IP Address found in output

       elif line.startswith("Host is"):
          HostStatus.append(line) # Append list of found Host status

    ListDevInfo = zip(IPHost,HostStatus)  #combine IPHost and HostStatus

    hosts = dict(zip(MACAdd,ListDevInfo)) #create dict of combined output

    print "******************************************************"
    print " "
    print "Active Connections:"
    print " "
    for key in sorted(hosts.iterkeys()):
            print "%s: %s" % (key, hosts[key]) #output of active connections to Network

    print " "

    print "******************************************************"
    print " "
    for line2 in parseNmap:
            if line2.startswith("Nmap done:"):
                print line2 # Number of Hosts 'UP' Status
    print " "
    print "******************************************************"
    print " "

    MACformat = re.compile('(?:[0-9a-fA-F]:?){12}') #Regex for MAC Address format

    for i in MACAdd:
            MACAddress = re.findall(MACformat,i)
            if MACAddress[0] in MACAllowedList: #Seaarching White List for Allowed Devices
               print MACAddress[0] + '\033[92m [AUTHORIZED ID]\033[0m'

            else:
              print MACAddress[0] + '\033[91m [WARNING: UNAUTHORIZED ID DETECTED!!!]\033[0m'  #Seaarching White List for Unauthorized Devices



    print " "
    print "******************************************************"






#Clean Code For GUI Programming/Command-Line Option as well.(Next To Do)