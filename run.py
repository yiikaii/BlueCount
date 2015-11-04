#!/usr/bin/python
import re 	# for Regex library

# Regex pattern for matching string in PCAP
# An example string in file is 741 572.433708 00:00:00_b8:89:84 -> 00:00:00_00:00:00 0xfff0 14 Ethernet II
# pattern only reads up to 741 572.433708 00:00:00_b8:89:84
pattern = re.compile("\s*\d{1,}\s*\d{1,}[.]\d{1,}\s*([0-9a-fA-F][0-9a-fA-F]:){2}[0-9a-fA-F][0-9a-fA-F][_](([0-9a-fA-F][0-9a-fA-F]:){2}([0-9a-fA-F][0-9a-fA-F]))")

# Using a dict to store LAP with keys as LAP so there will be no duplicates
mac_dict = {}

# Open txt file for reading only in binary format. The file pointer is placed at the beginning of the file. This is the default mode.
with open("openwithtshark.txt", "rb") as pcap_file:
    for line in pcap_file:

    	# Get a match from each line with the pattern
    	match_found = pattern.match(line)

    	if match_found:
    		# Store LAP entry to dict using LAP as key
    		mac_dict[match_found.group(2)] = match_found.group(2)

print "Total LAP found :", len(mac_dict)