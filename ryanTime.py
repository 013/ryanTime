#!/usr/bin/python

import re
import os
import time
import subprocess

def getUptime():
	proc = subprocess.Popen(["ps -eo pid,etime | sed -n 2p"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	
	y = re.search(r'(\d+-)?(\d+):(\d+):?(\d+)?', out).groups()
	
	days, hours, minutes, seconds = y
	
	if seconds == None:
		seconds = minutes
		minutes = hours
		hours = 0
	if days != None:
		days = int(days.split('-')[0])
	
	if days == None: days = 0
	if hours == None: hours = 0
	if minutes == None: minutes = 0
	if seconds == None: seconds = 0
			
	totalSeconds = int(seconds) + int(minutes)*60 + int(hours)*60*60 + int(days)*24*60*60

	# Uptime string #

	uptime = " " + time.strftime("%H:%M:%S") + " "

	updecades =	days / 3650
	upyears =	days / 365
	upweeks =	days / 7
	updays =	days
	
	uptime += "up "

	if updays:
		mdays = "s, " if updays != 1 else ", "
		uptime += str(updays) + " day" + mdays

	upminutes =	totalSeconds / 60
	uphours = 	upminutes / 60
	uphours =	uphours % 24
	upminutes =	upminutes % 60

	if uphours:
		uptime += str(uphours) + ":" + str(upminutes) + ", "
	else:
		uptime += str(upminutes) + " min, "

	# Users #
	proc = subprocess.Popen(["who | wc -l"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()

	users = int(out)

	musers = ", " if users == 1 else "s, "
	uptime += str(users) + " user" + musers

	# Load Average #
	loads = os.getloadavg()
	uptime += "load average: " + str(loads[0]) + ", " + str(loads[1]) + ", " + str(loads[2])

	return uptime

print getUptime()

