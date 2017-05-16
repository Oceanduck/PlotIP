#! /usr/bin/env python3
# usage map.py <ipfile>
# This script queries ipinfo.io and creates a csv file providind details of the IP Address
# Pass a file with one ip address on each line. Results would be written in Result.csv in the same folder. if ther is file with samename it would be deleted.

import os
import requests
import sys
import csv

file = csv.writer(open('Result.csv', 'w+'))
file.writerow(["ip", "city", "org", "loc", "country", "region",  "hostname"])
with open(sys.argv[1], 'r') as ipfile:
    for line in ipfile: 
        print(".", end='', flush=True)
        try:
            r = requests.get('http://ipinfo.io/'+line)
        except:
            print("cant Reach internet")
        ipP = r.json()
        try:
            if "bogon" in ipP:
                file.writerow([ipP["ip"],"BogonIP", "-", "-", "-", "-", "-"])
            else:
                file.writerow([ipP["ip"], ipP["city"], ipP["org"], ipP["loc"], ipP["country"], ipP["ip"], ipP["hostname"]])
        except:
            print("parsing error")
            print(ipP)
print("\nDone: Created file Results.csv")

