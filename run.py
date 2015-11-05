#!/usr/bin/python

import re
import threading
import os
import shutil
import subprocess
import sys

# Regex pattern for matching string in PCAP
# An example string in file is 741 572.433708 00:00:00_b8:89:84 -> 00:00:00_00:00:00 0xfff0 14 Ethernet II
# pattern only reads up to 741 572.433708 00:00:00_b8:89:84
pattern = re.compile("\s*\d{1,}\s*\d{1,}[.]\d{1,}\s*([0-9a-fA-F][0-9a-fA-F]:){2}[0-9a-fA-F][0-9a-fA-F][_](([0-9a-fA-F][0-9a-fA-F]:){2}([0-9a-fA-F][0-9a-fA-F]))")

# Using a dict to store LAP with keys as LAP so there will be no duplicates
mac_dict = {}

def printLapAddress():
	print "\nPrinting LAP Address\n===================="
	if len(mac_dict) > 0:
		for keys,values in mac_dict.items():
			print(keys)

def printLapCount():
	print "\nPrinting LAP count\n=================="
	print "Total count :", len(mac_dict)

def readFile():
	print "\nReading text file ...\n====================="
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
	print "\n>>> DONE"

def pipePcaptoText(pcapfile, textfile):
	try:
		print "\nUse tshark to read", pcapfile, "\n====================================="
		# read pcapbtbb file using wireshark and save to out
		out = subprocess.check_output(['tshark','r', pcapfile], stderr=subprocess.STDOUT)

		if out:
			print "\nSave output to", textfile

			# save out to text file
			with open(textfile, "w") as text_file:
				text_file.write(out)
			text_file.close()
			print "\n>>> DONE"

	except:
		print "ERROR: Invalid command"
		sys.exit(0)

def makeCopyOfPcapFile(new_filename):
	# set timer to repeat every 15 minutes
	#threading.Timer(900.0, renameFile).start()

	for filename in os.listdir("."):
		# find file name that starts with Kismet
		if filename.startswith("Kismet") and filename.endswith(".pcapbtbb"):
			print "\nMaking a copy of", filename, "to file", new_filename, "\n==============================================================================="
			# Copy file to another file
			shutil.copy2(filename, new_filename)
			
	print "\n>>> DONE"

def cleanup():
	print "\nRevert all operations on pcapbtbb file\n======================================"
	for filename in os.listdir("."):
		# find file name
		if filename == "bluecount.txt":
			os.remove(filename)
			print "Removed text file"
		if filename == "bluecount.pcapbtbb":
			os.remove(filename)
			print "Removed bluecount.pcapbtbb file"
	print "\n>>> DONE"

def run():
	# Set timer
	print "\nRun this in every 15 seconds"
	threading.Timer(15.0, run).start()

	makeCopyOfPcapFile("bluecount.pcapbtbb")
	pipePcaptoText("bluecount.pcapbtbb", "bluecount.txt")
	readFile()
	printLapAddress()
	printLapCount()
	cleanup()

run()