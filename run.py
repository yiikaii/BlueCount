#!/usr/bin/python
import re 	# for Regex library


'''
Step 1: Run Kismet 
Step 2: Rename pcapbtbb file name
Step 3: Run Wireshark
Step 4: Read txt file
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

def step4():
	# Open txt file for reading only in binary format. The file pointer is placed at the beginning of the file. This is the default mode.
    with open("openwithtshark.txt", "rb") as pcap_file:
        for line in pcap_file:

    	    # Get a match from each line with the pattern
    	    match_found = pattern.match(line)

    	    if match_found:
    	    	# Store LAP entry to dict using LAP as key
    	    	mac_dict[match_found.group(2)] = match_found.group(2)

#step4()
#printLapCount()
#printLapAddress()

def step1():
	import subprocess
	#subprocess.call(["ls", "-l", "/etc/resolv.conf"])

	#p = subprocess.Popen(["ls", "-l", "/etc/resolv.conf"], stdout=subprocess.PIPE)
	#output, err = p.communicate()

	prog_kismet = subprocess.Popen(["kismet"], stdout=subprocess.PIPE)
	output, err = prog_kismet.communicate()
	print "*** Running Kismet ***\n", output

def step2():
	import os

	for filename in os.listdir("."):
		#if filename.startswith("XXX"):
		if filename.endswith(".pcapbtbb"):
			os.rename(filename, "bluecount.pcapbtbb")

def step3():
	import subprocess
	#subprocess.call(["ls", "-l", "/etc/resolv.conf"])

	#p = subprocess.Popen(["ls", "-l", "/etc/resolv.conf"], stdout=subprocess.PIPE)
	#output, err = p.communicate()

	prog_kismet = subprocess.Popen(["wireshark", "-r", "xxx.pcapbtbb"], stdout=subprocess.PIPE)
	output, err = prog_kismet.communicate()
	print "*** Running Kismet ***\n", output

