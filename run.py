#!/usr/bin/python

import re
import os

'''
Step 1: Run Kismet 
'''
import subprocess
import sys

try: 
    subprocess.call(['kismet'])
except: 
    print "No Kismet executable found"
    sys.exit(0)


'''
Step 2: After running Kismet for 15 min, rename pcapbtbb file name. 

Read pcapbtbb file using wireshark and pipe to a text file.
This will repeat for every other 15 min when Kismet is still running
'''
import threading
import os
import shutil

def pipePcaptoText():
	try:
		# read pcapbtbb file using wireshark and pipe to text file
		subprocess.call(['tshark','r','bluecount.pcapbtbb','>','bluecount.txt'])
		
		print "Piped to text file, remove pcapbtbb file"
		
		# delete pcapbtbb after pipe
		if filename.startswith("bluecount"):
			os.remove(filename)

		# read file
		readFile()

		# print LAP count
		printLapCount()

		# print LAP addresses found
		printLapAddress()

	except:
		print "Invalid command"
		sys.exit(0)

def renameFile():
	# set timer to repeat every 15 minutes
	threading.Timer(900.0, renameFile).start()
	print "After 15 min, renaming pcapbtbb file ..."
	for filename in os.listdir("."):
		# find file name that starts with Kismet
		if filename.startswith("Kismet"):
			# Copy file to another file
			shutil.copy2(filename, 'bluecount.pcapbtbb')
			# Remove original file
			os.remove(filename)
			# open pcapbtbb file using wireshark and pipe to text file
			# delete pcapbtbb after pipe
			pipePcaptoText()


# Timer(seconds, call)
threading.Timer(900.0, renameFile).start()

'''
Step 3: Read txt file and output total cost of unique LAP captured
'''
# Regex pattern for matching string in PCAP
# An example string in file is 741 572.433708 00:00:00_b8:89:84 -> 00:00:00_00:00:00 0xfff0 14 Ethernet II
# pattern only reads up to 741 572.433708 00:00:00_b8:89:84
pattern = re.compile("\s*\d{1,}\s*\d{1,}[.]\d{1,}\s*([0-9a-fA-F][0-9a-fA-F]:){2}[0-9a-fA-F][0-9a-fA-F][_](([0-9a-fA-F][0-9a-fA-F]:){2}([0-9a-fA-F][0-9a-fA-F]))")

# Using a dict to store LAP with keys as LAP so there will be no duplicates
mac_dict = {}

def printLapAddress():
	if len(mac_dict) > 0:
		for keys,values in mac_dict.items():
			print(keys)

def printLapCount():
	print len(mac_dict)

def readFile():
	# Open txt file for reading only in binary format. The file pointer is placed at the beginning of the file. This is the default mode.
    with open("bluecount.txt", "rb") as pcap_file:
        for line in pcap_file:

    	    # Get a match from each line with the pattern
    	    match_found = pattern.match(line)

    	    if match_found:
    	    	# Store LAP entry to dict using LAP as key
    	    	mac_dict[match_found.group(2)] = match_found.group(2)

    # close file after read to free up any system resources taken up by the open file
    pcap_file.close()
