
#Date: October 23 2016


"""Description:
    This script can be used to investigate IP addressess that have been gathered as part of any investigation.
    Often investigators gather a list of IP Addresses that have been used in the attack.
    This script is designed to help the investigators to invetigate these IP addresses quickly.

    Functionality:
    The scripts performs the following functions:
    1. Extract information about location of the IP Address
    2. Plot the IP Address on a Map using Google API
    3. Check if the IP Address is a Tor Node
    4. Check the ASN detils of the IP Address

    Input:
    Script takes a text file as input, Each line should have one IP Address to be examined. Ips.txt is provided with the script as an example

    Output:
    The script genrates the following output in the folder passed on as -p (output directory)
    1. CSV File with Following details for the IP Address:
    2. An Image with the IP address plotted on a map (Using Google API)
    3. Open a web-browser with the map image

    Dependencies:
    1. GeoIP Database
    The script uses a free data base povided by maxmind for IP lookup. The database can be downloaded from
    http://dev.maxmind.com/geoip/geoip2/geolite2/.
    Download the GeoLite2-City.mmdb from the link for this python to work correctly.
    Disclaimer:
    This product includes GeoLite2 data created by MaxMind, available from http://www.maxmind.com

    2. This python script uses Google API to plot the ip address on a world map image. Pleae add your key in the script at googleApiKey = "Add Your Key here". If you create your API you would also need to enable it
    https://console.developers.google.com/projectselector/apis/api/static_maps_backend
    You can request a Google APi Key from Credentials link at https://developers.google.com/api-client-library/python/guide/aaa_apikeys
    URL length Restriction for Google Static Maps API is 8192 characters in size and maximum of 2500 requests.

    3. GeoIP2.database module: This script requires python module geoip2.database to work. This module can be installed using pip utility.
    $ pip install geoip2
"""

import geoip2.database        #Python Geoip2 Third Party Module, to be installed
import urllib                 #Python urllib module to work with urls
import csv                    #Python csv Module to I/O csv files
import datetime               #Python Module for Date and Time
import webbrowser             #Python Module to interact with Web Browser
import argparse               #Python Argument Parser module
import os                     #Python Modle for os


class CSVWriter:
    def __init__(self, outputFile):
        try:
            # create a writer object and then write the header row
            self.csvFile = open(outputFile, 'wb')
            self.writer = csv.writer(self.csvFile, delimiter=',', quoting=csv.QUOTE_ALL)
            self.writer.writerow( ('IP Address', 'GPS Long', 'GPS Lat', 'Country', 'State', 'City', 'Tor Status', 'ASN Info') )
        except:
            log.error('CSV File Failure')

    def writeCSVRow(self, Value):
        self.writer.writerow( (Value[0], Value[1], Value[2], Value[3], Value[4], Value[5], Value[6], Value[7] ) )

    def __del__(self):
        self.csvFile.close()

#Command Parser to pass out Directory and the file name as input.
def ParseCommandLine():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help="Set the Verbose Mode, This is Turned off by Default", action='store_true')
    parser.add_argument('-p', '--outPath', type=ValidateDirectory, required=True, help='Output Directory for the results')
    parser.add_argument('-f', '--fileName', type=ValidateFile, help='Input File to be parsed, This file should have IP Addressess One each per line',required=True)
    theArgs = parser.parse_args()
    if VERBOSE:
        print "Variables recieved and parsed", theArgs
 #   print theArgs
    return theArgs

# Validate if the file exists
def ValidateFile(theFile):
    if os.path.isfile(theFile):
        return theFile
    else:
        raise argparse.ArgumentTypeError('The file Does not exist')

# Validate if the directory exists and is writable
def ValidateDirectory(theDir):

    # Validate if the out dir exists
    if not os.path.isdir(theDir):
        raise argparse.ArgumentTypeError('Directory does not exist')

    # Validate the path is writable
    if os.access(theDir, os.W_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError('Directory is not writable')

# Get the IP Details from the IP Database directory
def ipInformation(line):
    if VERBOSE:
        print "Getting Information for IP Address", line
    ipList = []
    response = reader.city(line)
    ipLat = response.location.latitude
    ipLong = response.location.longitude
    ipCountry = response.country.name
    ipState = response.subdivisions.most_specific.name
    ipCity = response.city.name
    ipAddress = line
    ipList.extend([ipAddress, ipLat, ipLong, ipCountry, ipState, ipCity])
    return ipList

#Create a map file using Google API and store it as map.png. The function also opens a webbrowser link to the file
def mapFetch(urlParameter):
    if VERBOSE:
        print "Opening WebBrowser"
        print "Fetching the Map from Google"
    urlToFetch =  "https://maps.googleapis.com/maps/api/staticmap?center=0&scale=2&zoom=1&size=500x400&markers=color:red|size:tiny"+urlParameter+"&key="+googleApiKey
    if len(urlToFetch) < 8192:
        webbrowser.open(urlToFetch)
        urllib.urlretrieve(urlToFetch, "map.png")
    else:
        print "The length of the URL is greater than 8192, Reduce the accuracy of the GPS Coordinates"

#Check if the IP Address is part of the TOR Exit Node as of Today
def torCheck(IP, date):
    if VERBOSE:
        print "Checking Tor Exit Node for", IP
    url =  "https://exonerator.torproject.org/?"
    params = urllib.urlencode({'ip': IP, 'timestamp': date})
    openUrl = urllib.urlopen('%s%s'%(url,params)).read()
    if "did not find IP address" in openUrl:
        torStatus = "No"
    elif "found one or more Tor relays" in openUrl:
        torStatus = "Yes"
    else:
        torStatus = "unknown"
    return torStatus

#Check the ASN Number of the IP Address
def asnCheck(IP):
    if VERBOSE:
        print "Checking The ASN Number for IP Address", IP
    IP = IP.strip()
    openUrl = urllib.urlopen("http://ipinfo.io/"+IP+"/org")
    asnInfo = openUrl.read()
    return asnInfo.rstrip()



#Define Static Variables
reader = geoip2.database.Reader("/home/sansforensics/Desktop/Champlain/python/FinalProject/GeoLite2-City.mmdb")
# This is test API Key for the assignment only.

googleApiKey = "Add Your Key here"
urlParameter = ''
todayDate =datetime.datetime.now().date()
detailsList = []
VERBOSE = False
#Create a CSVWriter class, CSVWriter creates and manages csv files.

userArgs = ParseCommandLine()

#Set VERBOSE if the verbose mode is set
if userArgs.verbose:
    VERBOSE = True
else:
    VERBOSE = False


resultFile = os.path.join(userArgs.outPath,"plotIP-Results.csv")

oCSV = CSVWriter(resultFile)
fileName = userArgs.fileName
theFile = open(fileName, 'r')

for line in theFile:
    if VERBOSE:
        print "===================================="
        print "Processing IP Address", line.strip()
    detailsList = ipInformation(line.strip())
    urlParameter = urlParameter + '|'+ str(detailsList[1]) +',' + str(detailsList[2])
    torStatus = torCheck(line.strip(), todayDate)
    detailsList.append(torStatus)
    asnValue = asnCheck(line.strip())
    detailsList.append(asnValue)

    if VERBOSE:
        print "Writing the values to the CSV File"
    oCSV.writeCSVRow(detailsList)
if VERBOSE:
    print "===================================="
mapFetch(urlParameter)
print "Script Running Finished"
