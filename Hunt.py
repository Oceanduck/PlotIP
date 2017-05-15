#!/usr/bin/python3

import re
import sys
import os

#Python script to check for IP address. Two folders need to be created, One with the files with IP address that have been provided as part of any Intel Feeds and the other folder with logs. 

#Usage: hunt.py <IntelFolder> <LogFolder>
intelFolder = sys.argv[1]
logFolder = sys.argv[2]

#define regex for IP Address
ipRegex = re.compile(r'[123]*[0-9]*[0-9]\.[1,2]*[0-9]*[0-9]\.[1,2]*[0-9]*[0-9]\.[1,2]*[0-9]*[0-9]')

#Create two lists
intelIPList = []
logIPList = []
print("IntelSource, IP Match, Log File Matched")

#For each file in the Intel Directory create list intelIPList of tuples with (filename, IP Address)
for intelIPFile in os.listdir(os.path.join(os.getcwd(),intelFolder)):
    with open(os.path.join(os.getcwd(),intelFolder, intelIPFile)) as intelFile:
        for line in intelFile:
            IPsinLine = ipRegex.findall(line)
            for ip in IPsinLine:
                item = (os.path.basename(intelFile.name), ip)
                intelIPList.append(item)
            intelIPset = set(intelIPList)        

#Loop for Log Files
    for logIPFile in os.listdir(os.path.join(os.getcwd(), logFolder)):
        with open(os.path.join(os.getcwd(), logFolder, logIPFile)) as logFile:
            for line1 in logFile:
                IPsinLine1 = ipRegex.findall(line1)
                for ip1 in IPsinLine1:
                    logIPList.append(ip1)
            logFile.close()
        logSet = set(logIPList)
        for key,value in intelIPset:
            if value in logSet: 	        
                print(str(key)+', '+str(value)+', '+ str(logIPFile))
